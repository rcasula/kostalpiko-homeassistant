"""Adds config flow for Kostal."""

import logging
from typing import Any

from kostalpiko.kostalpiko import Piko
from requests.exceptions import ConnectTimeout, HTTPError
import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.const import (
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.util import slugify

from .configuration_schema import SENSOR_TYPE_KEY, UserInputType
from .const import DEFAULT_NAME, DOMAIN, SENSOR_TYPES

SUPPORTED_SENSOR_TYPES = list(SENSOR_TYPES)

DEFAULT_MONITORED_CONDITIONS: list[SENSOR_TYPE_KEY] = [
    SENSOR_TYPE_KEY.SENSOR_CURRENT_POWER,
    SENSOR_TYPE_KEY.SENSOR_TOTAL_ENERGY,
    SENSOR_TYPE_KEY.SENSOR_DAILY_ENERGY,
    SENSOR_TYPE_KEY.SENSOR_STATUS,
]

_LOGGER = logging.getLogger(__name__)


@callback
def kostal_entries(hass: HomeAssistant) -> set[str]:
    """Return the hosts for the domain."""
    return {
        (entry.data[CONF_HOST]) for entry in hass.config_entries.async_entries(DOMAIN)
    }


class KostalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kostal piko."""

    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self) -> None:
        """Initialize."""
        self._errors: dict[str, str] = {}

    def _host_in_configuration_exists(self, host: str) -> bool:
        """Return True if site_id exists in configuration."""
        if host in kostal_entries(self.hass):
            return True
        return False

    def _check_host(self, host: str, username: str, password: str) -> bool:
        """Check if we can connect to the kostal inverter."""
        piko = Piko(host, username, password)
        try:
            piko._get_info()  # pylint: disable=protected-access
        except (ConnectTimeout, HTTPError):
            self._errors[CONF_HOST] = "could_not_connect"
            return False

        return True

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        _user_input: UserInputType
        if user_input is not None:
            name = slugify(user_input.get(CONF_NAME, DEFAULT_NAME))
            if self._host_in_configuration_exists(user_input[CONF_HOST]):
                self._errors[CONF_HOST] = "host_exists"
            else:
                host = user_input[CONF_HOST]
                username = user_input[CONF_USERNAME]
                password = user_input[CONF_PASSWORD]
                conditions = user_input[CONF_MONITORED_CONDITIONS]
                can_connect = await self.hass.async_add_executor_job(
                    self._check_host, host, username, password
                )
                if can_connect:
                    return self.async_create_entry(
                        title=name,
                        data={
                            CONF_HOST: host,
                            CONF_USERNAME: username,
                            CONF_PASSWORD: password,
                            CONF_MONITORED_CONDITIONS: conditions,
                        },
                    )
            _user_input = user_input  # type: ignore
        else:
            _user_input = {
                CONF_NAME: DEFAULT_NAME,
                CONF_HOST: "http://",
                CONF_USERNAME: "",
                CONF_PASSWORD: "",
                CONF_MONITORED_CONDITIONS: DEFAULT_MONITORED_CONDITIONS,
            }

        default_monitored_conditions = (
            [] if self._async_current_entries() else DEFAULT_MONITORED_CONDITIONS
        )
        setup_schema = vol.Schema(
            {
                vol.Required(
                    CONF_NAME, default=_user_input.get(CONF_NAME, DEFAULT_NAME)
                ): str,
                vol.Required(CONF_HOST, default=_user_input[CONF_HOST]): str,  # type: ignore
                vol.Required(
                    CONF_USERNAME, description={"suggested_value": "pvserver"}
                ): str,
                vol.Required(CONF_PASSWORD, default=_user_input[CONF_PASSWORD]): str,  # type: ignore
                vol.Required(
                    CONF_MONITORED_CONDITIONS,
                    default=default_monitored_conditions,  # type: ignore
                ): cv.multi_select(SUPPORTED_SENSOR_TYPES),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=setup_schema, errors=self._errors
        )

    async def async_step_import(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Import a config entry."""
        if user_input is not None and self._host_in_configuration_exists(
            user_input[CONF_HOST]
        ):
            return self.async_abort(reason="host_exists")
        return await self.async_step_user(user_input)


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
