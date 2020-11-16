"""Kostal Piko Configuration Schemas."""

import voluptuous as vol

from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_MONITORED_CONDITIONS,
)

import homeassistant.helpers.config_validation as cv

from .const import DEFAULT_NAME, DOMAIN, SENSOR_TYPES

CONFIG_SCHEMA_ROOT = vol.Schema({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_MONITORED_CONDITIONS): vol.All(
        cv.ensure_list, [vol.In(list(SENSOR_TYPES))]
    ),
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: CONFIG_SCHEMA_ROOT
}, extra=vol.ALLOW_EXTRA)