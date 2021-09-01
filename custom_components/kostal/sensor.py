"""Support for Kostal PIKO Photvoltaic (PV) inverter."""

import logging, time
from .piko_holder import PikoHolder

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle, dt
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
    DEVICE_CLASS_ENERGY,
    ENERGY_KILO_WATT_HOUR,
)

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntity,
)

from .const import SENSOR_TYPES, MIN_TIME_BETWEEN_UPDATES, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry, async_add_entities):
    """Set up the sensor dynamically."""
    _LOGGER.info("Setting up kostal piko sensor")
    async def async_add_sensors(sensors, piko: PikoHolder):
        """Add a sensor."""
        info = await hass.async_add_executor_job(piko._get_info)
        _sensors = []
        for sensor in sensors:
            _sensors.append(PikoSensor(hass, piko, sensor, info, entry.title))
        
        async_add_entities(_sensors)
        # async_add_entities([
        #     PikoSensor(piko, type, entry.title)
        # ])

    async_dispatcher_connect(
        hass,
        "kostal_init_sensors",
        async_add_sensors
    )


class PikoSensor(SensorEntity):
    """Representation of a Piko inverter value."""

    def __init__(self,  hass: HomeAssistantType, piko: PikoHolder, sensor_type, info={None,None}, name=None):
        """Initialize the sensor."""
        _LOGGER.debug("Initializing PikoSensor: %s", sensor_type)
        self._sensor = SENSOR_TYPES[sensor_type][0]
        self._name = name
        self.hass = hass
        self.type = sensor_type
        self.piko = piko
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self.serial_number = info[0]
        self.model = info[1]
        if self._unit_of_measurement == ENERGY_KILO_WATT_HOUR:
            self._attr_state_class = STATE_CLASS_MEASUREMENT
            self._attr_device_class = DEVICE_CLASS_ENERGY
            if self._sensor == SENSOR_TYPES["daily_energy"][0]:
                self._attr_last_reset = dt.as_utc(dt.start_of_local_day())
            else:
                self._attr_last_reset = dt.utc_from_timestamp(0)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {}".format(self._name, self._sensor)

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return icon."""
        return self._icon

    @property
    def unique_id(self):
        """Return unique id based on device serial and variable."""
        return "{} {}".format(self.serial_number, self._sensor)

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self.serial_number)},
            "name": self._name,
            "manufacturer": "Kostal",
            "model": self.model,
        }


    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        await self.hass.async_add_executor_job(self._update)

    
    def _update(self):
        """Update data."""
        self.piko.update()
        data = self.piko.data
        ba_data = self.piko.ba_data

        if data is not None:
            if self.type == "current_power":
                self._state = data.get_current_power()
            elif self.type == "total_energy":
                self._state = data.get_total_energy()
            elif self.type == "daily_energy":
                self._state = data.get_daily_energy()
            elif self.type == "string1_voltage":
                self._state = data.get_string1_voltage()
            elif self.type == "string1_current":
                self._state = data.get_string1_current()
            elif self.type == "string2_voltage":
                self._state = data.get_string2_voltage()
            elif self.type == "string2_current":
                self._state = data.get_string2_current()
            elif self.type == "string3_voltage":
                self._state = data.get_string3_voltage()
            elif self.type == "string3_current":
                self._state = data.get_string3_current()
            elif self.type == "l1_voltage":
                self._state = data.get_l1_voltage()
            elif self.type == "l1_power":
                self._state = data.get_l1_power()
            elif self.type == "l2_voltage":
                self._state = data.get_l2_voltage()
            elif self.type == "l2_power":
                self._state = data.get_l2_power()
            elif self.type == "l3_voltage":
                self._state = data.get_l3_voltage()
            elif self.type == "l3_power":
                self._state = data.get_l3_power()
            elif self.type == "status":
                self._state = data.get_piko_status()
        if ba_data is not None:
            if self.type == "solar_generator_power":
                self._state = ba_data.get_solar_generator_power() or "No BA sensor installed"
            elif self.type == "consumption_phase_1":
                self._state = ba_data.get_consumption_phase_1() or "No BA sensor installed"
            elif self.type == "consumption_phase_2":
                self._state = ba_data.get_consumption_phase_2() or "No BA sensor installed"
            elif self.type == "consumption_phase_3":
                self._state = ba_data.get_consumption_phase_3() or "No BA sensor installed"

        _LOGGER.debug("END - Type: {} - {}".format(self.type, self._state))
