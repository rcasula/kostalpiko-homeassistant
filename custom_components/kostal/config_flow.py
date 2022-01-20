"""Adds config flow for Kostal."""

import logging
import voluptuous as vol

from kostalpiko.kostalpiko import Piko

from requests.exceptions import HTTPError, ConnectTimeout

from homeassistant import config_entries, exceptions
import homeassistant.helpers.config_validation as cv

from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_MONITORED_CONDITIONS,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.util import slugify

from .const import DOMAIN, DEFAULT_NAME, SENSOR_TYPES

SUPPORTED_SENSOR_TYPES = list(SENSOR_TYPES)

DEFAULT_MONITORED_CONDITIONS = [
    "current_power",
    "total_energy",
    "daily_energy",
    "status",
]

_LOGGER = logging.getLogger(__name__)

@callback
def kostal_entries(hass: HomeAssistant):
    """Return the hosts for the domain."""
    return set(
        (entry.data[CONF_HOST]) for entry in hass.config_entries.async_entries(DOMAIN)
    )

class KostalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kostal piko."""

    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    def _host_in_configuration_exists(self, host) -> bool:
        """Return True if site_id exists in configuration."""
        if host in kostal_entries(self.hass):
            return True
        return False

    def _check_host(self, host, username, password) -> bool:
        """Check if we can connect to the kostal inverter."""
        piko = Piko(host, username, password)
        try:
            response = piko._get_info()
        except (ConnectTimeout, HTTPError):
            self._errors[CONF_HOST] = "could_not_connect"
            return False

        return True

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

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
        else:
            user_input = {}
            user_input[CONF_NAME] = DEFAULT_NAME
            user_input[CONF_HOST] = "http://"
            user_input[CONF_USERNAME] = ""
            user_input[CONF_PASSWORD] = ""
            user_input[CONF_MONITORED_CONDITIONS] = DEFAULT_MONITORED_CONDITIONS

        default_monitored_conditions = (
            [] if self._async_current_entries() else DEFAULT_MONITORED_CONDITIONS
        )
        setup_schema = vol.Schema(
            {
                vol.Required(
                    CONF_NAME, default=user_input.get(CONF_NAME, DEFAULT_NAME)
                ): str,
                vol.Required(CONF_HOST, default=user_input[CONF_HOST]): str,
                vol.Required(
                    CONF_USERNAME, description={"suggested_value": "pvserver"}
                ): str,
                vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                vol.Required(
                    CONF_MONITORED_CONDITIONS, default=default_monitored_conditions
                ): cv.multi_select(SUPPORTED_SENSOR_TYPES),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=setup_schema, errors=self._errors
        )

    async def async_step_import(self, user_input=None):
        """Import a config entry."""
        if self._host_in_configuration_exists(user_input[CONF_HOST]):
            return self.async_abort(reason="host_exists")
        return await self.async_step_user(user_input)


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
