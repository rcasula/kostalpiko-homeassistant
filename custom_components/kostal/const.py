"""Constants for the Kostal piko integration."""
from datetime import timedelta

from homeassistant.const import (
    POWER_WATT,
    ENERGY_KILO_WATT_HOUR,
    VOLT,
    ELECTRICAL_CURRENT_AMPERE,
)

DOMAIN = "kostal"

DEFAULT_NAME = "Kostal Piko"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

SENSOR_TYPES = {
    "solar_generator_power": ["Solar generator power", POWER_WATT, "mdi:solar-power"],
    "consumption_phase_1": ["Consumption phase 1", POWER_WATT, "mdi:power-socket-eu"],
    "consumption_phase_2": ["Consumption phase 2", POWER_WATT, "mdi:power-socket-eu"],
    "consumption_phase_3": ["Consumption phase 3", POWER_WATT, "mdi:power-socket-eu"],
    "current_power": ["Current power", POWER_WATT, "mdi:solar-power"],
    "total_energy": ["Total energy", ENERGY_KILO_WATT_HOUR, "mdi:solar-power"],
    "daily_energy": ["Daily energy", ENERGY_KILO_WATT_HOUR, "mdi:solar-power"],
    "string1_voltage": ["String 1 voltage", VOLT, "mdi:current-ac"],
    "string1_current": ["String 1 current", ELECTRICAL_CURRENT_AMPERE, "mdi:flash"],
    "string2_voltage": ["String 2 voltage", VOLT, "mdi:current-ac"],
    "string2_current": ["String 2 current", ELECTRICAL_CURRENT_AMPERE, "mdi:flash"],
    "string3_voltage": ["String 3 voltage", VOLT, "mdi:current-ac"],
    "string3_current": ["String 3 current", ELECTRICAL_CURRENT_AMPERE, "mdi:flash"],
    "l1_voltage": ["L1 voltage", VOLT, "mdi:current-ac"],
    "l1_power": ["L1 power", POWER_WATT, "mdi:power-plug"],
    "l2_voltage": ["L2 voltage", VOLT, "mdi:current-ac"],
    "l2_power": ["L2 power", POWER_WATT, "mdi:power-plug"],
    "l3_voltage": ["L3 voltage", VOLT, "mdi:current-ac"],
    "l3_power": ["L3 power", POWER_WATT, "mdi:power-plug"],
    "status": ["Status", None, "mdi:solar-power"],
}