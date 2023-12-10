"""Support for Kostal PIKO Photvoltaic (PV) inverter."""
import logging
from typing import TypedDict

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import Throttle

from .configuration_schema import SENSOR_TYPE_KEY
from .const import DOMAIN, MIN_TIME_BETWEEN_UPDATES, SENSOR_TYPES
from .piko_holder import PikoHolder

_LOGGER = logging.getLogger(__name__)


class KostalDeviceInfo(TypedDict):
    """Device info from Kostal."""

    serial: str
    model: str | None


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor dynamically."""
    _LOGGER.info("Setting up kostal piko sensor")

    async def async_add_sensors(
        sensors: list[SENSOR_TYPE_KEY], piko: PikoHolder
    ) -> None:
        """Add a sensor."""
        _info: list[str] | None = await hass.async_add_executor_job(piko._get_info)  # pylint: disable=protected-access
        info: KostalDeviceInfo = {
            "serial": entry.data.get("host", "UNKNOWN"),
            "model": None,
        }
        if _info is not None:
            info = {"serial": _info[0], "model": _info[1]}
        _sensors = []
        for sensor in sensors:
            _sensors.append(PikoSensor(hass, piko, sensor, info, entry.title))

        async_add_entities(_sensors)
        # async_add_entities([
        #     PikoSensor(piko, type, entry.title)
        # ])

    async_dispatcher_connect(
        hass, "kostal_init_sensors_" + entry.entry_id, async_add_sensors
    )


class PikoSensor(SensorEntity):
    """Representation of a Piko inverter value."""

    def __init__(
        self,
        hass: HomeAssistant,
        piko: PikoHolder,
        sensor_type: SENSOR_TYPE_KEY,
        info: KostalDeviceInfo,
        name: str | None = None,
    ) -> None:
        """Initialize the sensor."""
        _LOGGER.debug("Initializing PikoSensor: %s", sensor_type)
        self._sensor = SENSOR_TYPES[sensor_type]["name"]
        self._name = name
        self.hass = hass
        self.type = sensor_type
        self.piko = piko
        # self._state: float | int | str | None = None
        self._attr_native_unit_of_measurement = SENSOR_TYPES[self.type]["unit"]
        self._attr_icon = SENSOR_TYPES[self.type]["icon"]
        self._attr_name = f"{name} {self._sensor}"
        self._attr_unique_id = f"{info['serial']} {self._sensor}"
        self.kostal_info = info
        if SENSOR_TYPES[self.type]["unit"] == UnitOfEnergy.KILO_WATT_HOUR:
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    # @property
    # def state(self) -> str | float | int | None:
    #     """Return the state of the device."""
    #     return self._state

    @property
    def device_info(self) -> DeviceInfo:
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self.kostal_info["serial"])},
            "name": self._name,
            "manufacturer": "Kostal",
            "model": self.kostal_info["model"],
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self) -> None:
        """Update kostal entity async."""
        await self.hass.async_add_executor_job(self._update)

    def _update(self) -> None:
        """Update kostal entity."""
        self.piko.update()
        data = self.piko.data
        ba_data = self.piko.ba_data
        value: int | float | str | None = None
        if data is not None:
            if self.type == "current_power":
                value = data.get_current_power()
            elif self.type == "total_energy":
                value = data.get_total_energy()
            elif self.type == "daily_energy":
                value = data.get_daily_energy()
            elif self.type == "string1_voltage":
                value = data.get_string1_voltage()
            elif self.type == "string1_current":
                value = data.get_string1_current()
            elif self.type == "string2_voltage":
                value = data.get_string2_voltage()
            elif self.type == "string2_current":
                value = data.get_string2_current()
            elif self.type == "string3_voltage":
                value = data.get_string3_voltage()
            elif self.type == "string3_current":
                value = data.get_string3_current()
            elif self.type == "l1_voltage":
                value = data.get_l1_voltage()
            elif self.type == "l1_power":
                value = data.get_l1_power()
            elif self.type == "l2_voltage":
                value = data.get_l2_voltage()
            elif self.type == "l2_power":
                value = data.get_l2_power()
            elif self.type == "l3_voltage":
                value = data.get_l3_voltage()
            elif self.type == "l3_power":
                value = data.get_l3_power()
            elif self.type == "status":
                value = data.get_piko_status()
        if ba_data is not None:
            if self.type == "solar_generator_power":
                value = ba_data.get_solar_generator_power() or "No BA sensor installed"
            elif self.type == "consumption_phase_1":
                value = ba_data.get_consumption_phase_1() or "No BA sensor installed"
            elif self.type == "consumption_phase_2":
                value = ba_data.get_consumption_phase_2() or "No BA sensor installed"
            elif self.type == "consumption_phase_3":
                value = ba_data.get_consumption_phase_3() or "No BA sensor installed"
        self._attr_native_value = value
        _LOGGER.debug("END - Type: %s - %s", self.type, value)
