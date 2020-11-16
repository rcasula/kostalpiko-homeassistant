"""The Kostal PIKO inverter sensor integration."""

import logging

from kostalpiko.kostalpiko import Piko

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.dispatcher import async_dispatcher_send, dispatcher_send

from .const import DEFAULT_NAME, DOMAIN, SENSOR_TYPES
from .configuration_schema import CONFIG_SCHEMA, CONFIG_SCHEMA_ROOT

from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
    EVENT_HOMEASSISTANT_STOP
)

_LOGGER = logging.getLogger(__name__)

__version__ = "0.0.1"
VERSION = __version__


async def async_setup(hass, config):
    """Set up this integration using yaml."""
    _LOGGER.info("Setup kostal, %s", __version__)
    if DOMAIN not in config:
        return True

    data = dict(config.get(DOMAIN))
    hass.data["yaml_kostal"] = data

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=dict(config[DOMAIN])
        )
    )
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Setup KostalPiko component"""

    _LOGGER.info("Starting kostal, %s", __version__)

    if not DOMAIN in hass.data:
        hass.data[DOMAIN] = {}

    if entry.source == "import":
        if entry.options:  # config.yaml
            data = entry.options.copy()
        else:
            if "yaml_kostal" in hass.data:
                data = hass.data["yaml_kostal"]
            else:
                data = {}
                await hass.config_entries.async_remove(entry.entry_id)
    else:
        data = entry.data.copy()
        data.update(entry.options)

    conf = CONFIG_SCHEMA_ROOT(data)

    hass.data[DOMAIN][entry.entry_id] = KostalInstance(hass, entry, conf)
    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    instance = hass.data[DOMAIN][entry.entry_id]
    await instance.stop()
    await instance.clean()
    return True


class KostalInstance():
    """Config instance of Kostal"""

    def __init__(self, hass: HomeAssistantType, entry: ConfigEntry, conf):
        self.hass = hass
        self.config_entry = entry
        self.entry_id = self.config_entry.entry_id
        self.conf = conf
        self.piko = Piko(
            conf[CONF_HOST], conf[CONF_USERNAME], conf[CONF_PASSWORD]
        )

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.stop)

        hass.loop.create_task(
            self.start_up()
        )

    async def start_up(self):
        self.piko.update()
        self.add_sensors(self.conf[CONF_MONITORED_CONDITIONS], self.piko)

    async def stop(self, _=None):
        """Stop Kostal."""
        _LOGGER.info("Shutting down Kostal")

    def add_sensors(self, sensors, piko: Piko):
        self.hass.add_job(self._asyncadd_sensors(sensors, piko))

    async def _asyncadd_sensors(self, sensors, piko: Piko):
        await self.hass.config_entries.async_forward_entry_setup(self.config_entry, "sensor")
        async_dispatcher_send(self.hass, "kostal_init_sensors", sensors, piko)

    async def clean(self):
        pass
