#config.py

import math

# Panel Parameters
PANEL_RATING = 100.0                # kW
PANEL_EFFICIENCY = 0.82             # Accounts for inverter, wiring, and DC-to-AC conversion losses

# Dust / Soiling Parameters
DUST_TODAY = 0.0                    # Initial dust coverage (%) - starting clean
MAX_DUST = 25.0                     # Threshold where manual cleaning is triggered
DUST_LOSS_PER_PERCENT = 0.0033      # ~30% dust coverage results in ~10% max power loss

# Time Parameters
SUNRISE = 6
SUNSET = 18
DAYS = 7
HOURS_PER_DAY = 24

# Cloud Parameters
CLOUD_POWER_REDUCTION = 0.40                 # Passing clouds block 40% of sunlight
TEMPORARY_CLOUD_PROBABILITY_CLEAR = 0.10     # 10% chance cloud appears during a clear hour
TEMPORARY_CLOUD_PROBABILITY_CLOUD = 0.30     # 30% chance an existing cloud lingers into the next hour

# Load Parameters
BASE_LOAD = 25.0                     # kW

# Afternoon Peak(13:00)
AFTERNOON_PEAK_POWER = 15.0          # kW
AFTERNOON_PEAK_HOUR = 13             # 1 PM
AFTERNOON_PEAK_WIDTH = 2.5           # Wider standard deviation for staggered occupancy

# Evening Peak(19:30)
EVENING_PEAK_POWER = 45.0            # kW
EVENING_PEAK_HOUR = 19.5             
EVENING_PEAK_WIDTH = 3.0             

# Battery Parameters
BATTERY_CAPACITY = 200.0                # kWh 

BATTERY_CHARGE_EFFICIENCY = 0.95
BATTERY_DISCHARGE_EFFICIENCY = 0.95

BATTERY_MAX_CHARGE_RATE = 50.0          # kW 
BATTERY_MAX_DISCHARGE_RATE = 60.0       # kW 

BATTERY_ENERGY = 80.0                   # Initial Energy (kWh)
MINIMUM_SOC = 0.40                      # Minimum SoC to maintain battery health(40%)
MINIMUM_ENERGY = BATTERY_CAPACITY * MINIMUM_SOC   # 80 kWh

# Grid Parameters
GRID_BUY_PRICE = 5.5      # ₹/kWh 
GRID_SELL_PRICE = 5.5     # ₹/kWh 