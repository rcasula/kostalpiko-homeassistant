"""Kostal Piko Configuration Schemas."""
from typing import TypedDict

import voluptuous as vol

from homeassistant.const import (
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_USERNAME,
)
import homeassistant.helpers.config_validation as cv

from .const import DEFAULT_NAME, DOMAIN, SENSOR_TYPE_KEY, SENSOR_TYPES


class UserInputType(TypedDict):
    """Data entered by user."""

    name: str
    host: str
    username: str
    password: str
    monitored_conditions: list[SENSOR_TYPE_KEY]


CONFIG_SCHEMA_ROOT = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,  # type: ignore
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_MONITORED_CONDITIONS): vol.All(
            cv.ensure_list, [vol.In(list(SENSOR_TYPES))]
        ),
    }
)

CONFIG_SCHEMA = vol.Schema({DOMAIN: CONFIG_SCHEMA_ROOT}, extra=vol.ALLOW_EXTRA)
