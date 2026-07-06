# environment.py
import random
from enum import Enum
from sim_config import (
    MAX_DUST, 
    TEMPORARY_CLOUD_PROBABILITY_CLEAR, 
    TEMPORARY_CLOUD_PROBABILITY_CLOUD
)
class Weather(Enum):
    Clear = 0
    PartlyCloudy = 1
    Cloudy = 2

class Cleaned_frac(Enum):
    No_Rain = 0
    Light_40 = 1
    Moderate_60 = 2
    Heavy_100 = 3

class Will_rain(Enum):
    No_Rain = 0
    Yes = 1

TRANSITION_MATRIX = [
    [0.80, 0.20, 0.00],  
    [0.45, 0.10, 0.45],  
    [0.25, 0.65, 0.10]   
]

WEATHER_STATES = list(Weather)


def simulate_weather(today):
    weather_probabilities = TRANSITION_MATRIX[today.value]
    tomorrow = random.choices(
        WEATHER_STATES,
        weights=weather_probabilities
    )[0]
    return today, tomorrow


def simulate_rain(today):
    if today == Weather.PartlyCloudy:
        rain_today = random.choices(
            list(Will_rain),
            weights=[0.85, 0.15]
        )[0]
    elif today == Weather.Cloudy:
        rain_today = random.choices(
            list(Will_rain),
            weights=[0.40, 0.60]
        )[0]
    else:
        rain_today = Will_rain.No_Rain

    if rain_today == Will_rain.Yes:
        rain_type = random.choices(
            list(Cleaned_frac),
            weights=[0.00, 0.50, 0.35, 0.15]
        )[0]
    else:
        rain_type = Cleaned_frac.No_Rain

    return rain_today, rain_type


def simulate_dust(dust_today, rain_type):
    manual_cleaning = False

    # Dust evaluated every 6 hours
    for _ in range(4):
        dust_today += random.choices(
            [0.0, 0.1, 0.25, 0.5],
            weights=[0.50, 0.35, 0.12, 0.03]
        )[0]

    if rain_type == Cleaned_frac.Light_40:
        dust_today *= 0.60
    elif rain_type == Cleaned_frac.Moderate_60:
        dust_today *= 0.40
    elif rain_type == Cleaned_frac.Heavy_100:
        dust_today = 0.0

    if dust_today > MAX_DUST:
        dust_today = 0.0
        manual_cleaning = True

    return dust_today, manual_cleaning


def update_cloud_state(cloud_active):
    if not cloud_active:
        if random.random() < TEMPORARY_CLOUD_PROBABILITY_CLEAR:
            cloud_active = True
    else:
        if random.random() < TEMPORARY_CLOUD_PROBABILITY_CLOUD:
            cloud_active = True
        else:
            cloud_active = False

    return cloud_active