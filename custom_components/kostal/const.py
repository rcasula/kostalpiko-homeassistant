"""Constants for the Kostal piko integration."""
from datetime import timedelta
from enum import StrEnum
from typing import Final, TypedDict

from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)

DOMAIN = "kostal"

DEFAULT_NAME = "Kostal Piko"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)


class SensorDefinition(TypedDict):
    """Description of a sensor entity."""

    name: str
    unit: str | None
    icon: str


class SENSOR_TYPE_KEY(StrEnum):
    """Sensor type keys."""

    SENSOR_SOLAR_GENERATOR_POWER: Final = "solar_generator_power"
    SENSOR_CONSUMPTION_PHASE_1: Final = "consumption_phase_1"
    SENSOR_CONSUMPTION_PHASE_2: Final = "consumption_phase_2"
    SENSOR_CONSUMPTION_PHASE_3: Final = "consumption_phase_3"
    SENSOR_CURRENT_POWER: Final = "current_power"
    SENSOR_DAILY_ENERGY: Final = "daily_energy"
    SENSOR_TOTAL_ENERGY: Final = "total_energy"
    SENSOR_STRING1_VOLTAGE: Final = "string1_voltage"
    SENSOR_STRING2_VOLTAGE: Final = "string2_voltage"
    SENSOR_STRING3_VOLTAGE: Final = "string3_voltage"
    SENSOR_L1_VOLTAGE: Final = "l1_voltage"
    SENSOR_L2_VOLTAGE: Final = "l2_voltage"
    SENSOR_L3_VOLTAGE: Final = "l3_voltage"
    SENSOR_STRING1_CURRENT: Final = "string1_current"
    SENSOR_STRING2_CURRENT: Final = "string2_current"
    SENSOR_STRING3_CURRENT: Final = "string3_current"
    SENSOR_L1_CURRENT: Final = "l1_current"
    SENSOR_L2_CURRENT: Final = "l2_current"
    SENSOR_L3_CURRENT: Final = "l3_current"
    SENSOR_L1_POWER: Final = "l1_power"
    SENSOR_L2_POWER: Final = "l2_power"
    SENSOR_L3_POWER: Final = "l3_power"
    SENSOR_STATUS: Final = "status"


SENSOR_TYPES: dict[SENSOR_TYPE_KEY, SensorDefinition] = {
    SENSOR_TYPE_KEY.SENSOR_SOLAR_GENERATOR_POWER: {
        "name": "Solar generator power",
        "unit": UnitOfPower.WATT,
        "icon": "mdi:solar-power",
    },
    SENSOR_TYPE_KEY.SENSOR_CONSUMPTION_PHASE_1: {
        "name": "Consumption phase 1",
        "unit": UnitOfPower.WATT,
        "icon": "mdi:power-socket-eu",
    },
    SENSOR_TYPE_KEY.SENSOR_CONSUMPTION_PHASE_2: {
        "name": "Consumption phase 2",
        "unit": UnitOfPower.WATT,
        "icon": "mdi:power-socket-eu",
    },
    SENSOR_TYPE_KEY.SENSOR_CONSUMPTION_PHASE_3: {
        "name": "Consumption phase 3",
        "unit": UnitOfPower.WATT,
        "icon": "mdi:power-socket-eu",
    },
    SENSOR_TYPE_KEY.SENSOR_CURRENT_POWER: {
        "name": "Current power",
        "unit": UnitOfPower.WATT,
        "icon": "mdi:solar-power",
    },
    SENSOR_TYPE_KEY.SENSOR_TOTAL_ENERGY: {
        "name": "Total energy",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "icon": "mdi:solar-power",
    },
    SENSOR_TYPE_KEY.SENSOR_DAILY_ENERGY: {
        "name": "Daily energy",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "icon": "mdi:solar-power",
    },
    SENSOR_TYPE_KEY.SENSOR_STRING1_VOLTAGE: {
        "name": "String 1 voltage",
        "unit": UnitOfElectricPotential.VOLT,
        "icon": "mdi:current-ac",
    },
    SENSOR_TYPE_KEY.SENSOR_STRING1_CURRENT: {
        "name": "String 1 current",
        "unit": UnitOfElectricCurrent.AMPERE,
        "icon": "mdi:flash",
    },
    SENSOR_TYPE_KEY.SENSOR_STRING2_VOLTAGE: {
        "name": "String 2 voltage",
        "unit": UnitOfElectricPotential.VOLT,
        "icon": "mdi:current-ac",
    },
    SENSOR_TYPE_KEY.SENSOR_STRING2_CURRENT: {
        "name": "String 2 current",
        "unit": UnitOfElectricCurrent.AMPERE,
        "icon": "mdi:flash",
    },
    SENSOR_TYPE_KEY.SENSOR_STRING3_VOLTAGE: {
        "name": "String 3 voltage",
        "unit": UnitOfElectricPotential.VOLT,
        "icon": "mdi:current-ac",
    },
    SENSOR_TYPE_KEY.SENSOR_STRING3_CURRENT: {
        "name": "String 3 current",
        "unit": UnitOfElectricCurrent.AMPERE,
        "icon": "mdi:flash",
    },
    SENSOR_TYPE_KEY.SENSOR_L1_VOLTAGE: {
        "name": "L1 voltage",
        "unit": UnitOfElectricPotential.VOLT,
        "icon": "mdi:current-ac",
    },
    SENSOR_TYPE_KEY.SENSOR_L1_POWER: {
        "name": "L1 power",
        "unit": UnitOfPower.WATT,
        "icon": "mdi:power-plug",
    },
    SENSOR_TYPE_KEY.SENSOR_L2_VOLTAGE: {
        "name": "L2 voltage",
        "unit": UnitOfElectricPotential.VOLT,
        "icon": "mdi:current-ac",
    },
    SENSOR_TYPE_KEY.SENSOR_L2_POWER: {
        "name": "L2 power",
        "unit": UnitOfPower.WATT,
        "icon": "mdi:power-plug",
    },
    SENSOR_TYPE_KEY.SENSOR_L3_VOLTAGE: {
        "name": "L3 voltage",
        "unit": UnitOfElectricPotential.VOLT,
        "icon": "mdi:current-ac",
    },
    SENSOR_TYPE_KEY.SENSOR_L3_POWER: {
        "name": "L3 power",
        "unit": UnitOfPower.WATT,
        "icon": "mdi:power-plug",
    },
    SENSOR_TYPE_KEY.SENSOR_STATUS: {
        "name": "Status",
        "unit": None,
        "icon": "mdi:solar-power",
    },
}
