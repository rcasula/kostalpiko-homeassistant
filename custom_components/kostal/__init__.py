"""The Kostal PIKO inverter sensor integration."""
import logging
from typing import Any

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
    CONF_PASSWORD,
    CONF_USERNAME,
    EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.typing import ConfigType

from .configuration_schema import CONFIG_SCHEMA_ROOT, SENSOR_TYPE_KEY, UserInputType
from .const import DOMAIN
from .piko_holder import PikoHolder

_LOGGER = logging.getLogger(__name__)

__version__ = "1.3.0"
VERSION = __version__


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up this integration using yaml."""
    _LOGGER.info("Setup kostal, %s", __version__)
    if DOMAIN not in config:
        return True

    data = config.get(DOMAIN, {})
    hass.data["yaml_kostal"] = data

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=dict(config[DOMAIN])
        )
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Create KostalPiko component for config entry."""

    _LOGGER.info("Starting kostal, %s", __version__)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    if entry.source == "import":
        if entry.options:  # config.yaml
            data = entry.options.copy()
        elif "yaml_kostal" in hass.data:
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


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    instance: KostalInstance = hass.data[DOMAIN][entry.entry_id]
    await instance.stop()
    await instance.clean()
    return True


class KostalInstance:
    """Config instance of Kostal."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, conf: UserInputType
    ) -> None:
        """Create a new Kostal instance."""
        self.hass = hass
        self.config_entry = entry
        self.entry_id = self.config_entry.entry_id
        self.conf = conf
        self.piko = PikoHolder(
            conf[CONF_HOST], conf[CONF_USERNAME], conf[CONF_PASSWORD]
        )

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.stop)

        hass.loop.create_task(self.start_up())

    async def start_up(self) -> None:
        """Start the KOSTAL instance."""
        await self.hass.async_add_executor_job(self.piko.update)
        self.add_sensors(self.conf[CONF_MONITORED_CONDITIONS], self.piko)

    async def stop(self, _: Any = None) -> None:
        """Stop the KOSTAL instance."""
        _LOGGER.info("Shutting down Kostal")

    def add_sensors(self, sensors: list[SENSOR_TYPE_KEY], piko: PikoHolder) -> None:
        """Add sensors to HASS."""
        self.hass.add_job(self._asyncadd_sensors(sensors, piko))

    async def _asyncadd_sensors(
        self, sensors: list[SENSOR_TYPE_KEY], piko: PikoHolder
    ) -> None:
        """Add async sensors to HASS."""
        await self.hass.config_entries.async_forward_entry_setup(
            self.config_entry, "sensor"
        )
        async_dispatcher_send(
            self.hass,
            "kostal_init_sensors_" + self.config_entry.entry_id,
            sensors,
            piko,
        )

    async def clean(self) -> None:
        """Cleanup. Not implemented."""
