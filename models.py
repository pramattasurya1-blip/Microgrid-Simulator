# models.py
import math
# Add a dot before config
from sim_config import (
    PANEL_RATING, PANEL_EFFICIENCY, CLOUD_POWER_REDUCTION, DUST_LOSS_PER_PERCENT,
    SUNRISE, SUNSET, BASE_LOAD, AFTERNOON_PEAK_POWER, AFTERNOON_PEAK_HOUR, AFTERNOON_PEAK_WIDTH,
    EVENING_PEAK_POWER, EVENING_PEAK_HOUR, EVENING_PEAK_WIDTH,
    BATTERY_CAPACITY, BATTERY_CHARGE_EFFICIENCY, BATTERY_DISCHARGE_EFFICIENCY,
    BATTERY_MAX_CHARGE_RATE, BATTERY_MAX_DISCHARGE_RATE, MINIMUM_ENERGY
)
from weather import Weather

def simulate_solar(today, dust_today, current_hour, cloud_active, is_cleaning_downtime=False):
    # If manual cleaning is active, the system is fully offline for maintenance
    if is_cleaning_downtime:
        return 0.0, 0.0, 0.0, 0.0, False

    
    weather_reduction = 0.0
    temporary_cloud_event = False

    if today == Weather.PartlyCloudy:
        weather_reduction = 0.15
    elif today == Weather.Cloudy:
        weather_reduction = 0.20
    
    if cloud_active:
        temporary_cloud_event = True
        weather_reduction = max(weather_reduction, CLOUD_POWER_REDUCTION)
    # Micro-clouds can temporarily block light regardless of the macro day profile

    # Half-Sine Clear-Sky Irradiance Curve
    if SUNRISE <= current_hour <= SUNSET:
        theta = math.pi * (current_hour - SUNRISE) / (SUNSET - SUNRISE)
        irradiance = math.sin(theta)
        ideal_power = PANEL_RATING * irradiance * PANEL_EFFICIENCY
    else:
        irradiance = 0.0
        ideal_power = 0.0

    #Soiling Loss
    soiling_loss = min(dust_today * DUST_LOSS_PER_PERCENT, 0.10)

    # Output
    weather_factor = 1 - weather_reduction
    actual_power = ideal_power * weather_factor * (1 - soiling_loss)

    return (
        ideal_power,
        actual_power,
        irradiance,
        soiling_loss,
        temporary_cloud_event
    )


def simulate_load(current_hour):
    afternoon_peak = (
        AFTERNOON_PEAK_POWER *
        math.exp(-((current_hour - AFTERNOON_PEAK_HOUR) ** 2) / (2 * AFTERNOON_PEAK_WIDTH ** 2))
    )

    evening_peak = (
        EVENING_PEAK_POWER *
        math.exp(-((current_hour - EVENING_PEAK_HOUR) ** 2) / (2 * EVENING_PEAK_WIDTH ** 2))
    )

    return BASE_LOAD + afternoon_peak + evening_peak


def charge_battery(battery_energy, excess_power):
    charge_power = min(excess_power, BATTERY_MAX_CHARGE_RATE)
    available_capacity = BATTERY_CAPACITY - battery_energy
    
    energy_stored = min(
        charge_power * BATTERY_CHARGE_EFFICIENCY,
        available_capacity)
    
    battery_energy += energy_stored
    charging_power = energy_stored / BATTERY_CHARGE_EFFICIENCY
    grid_export = excess_power - charging_power

    return battery_energy, charging_power, grid_export


def discharge_battery(battery_energy, deficit_power):

    discharge_power = min(deficit_power, BATTERY_MAX_DISCHARGE_RATE)
    required_energy = discharge_power / BATTERY_DISCHARGE_EFFICIENCY

    available_energy = max(0, battery_energy - MINIMUM_ENERGY)
    energy_removed = min(required_energy, available_energy)

    battery_energy -= energy_removed
    supplied_power = energy_removed * BATTERY_DISCHARGE_EFFICIENCY
    grid_import = deficit_power - supplied_power

    return battery_energy, supplied_power, grid_import