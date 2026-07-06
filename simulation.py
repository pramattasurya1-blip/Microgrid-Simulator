# simulation.py

import sim_config
from weather import Weather, simulate_weather, simulate_rain, simulate_dust, update_cloud_state
from models import simulate_solar, simulate_load, charge_battery, discharge_battery

def run_weekly_simulation():
    
    dust_today = sim_config.DUST_TODAY
    battery_energy_current = sim_config.BATTERY_ENERGY
    today = Weather.Clear
    cloud_active = False
    
    cleaning_triggered_yesterday = False

    total_grid_import = 0.0
    total_grid_export = 0.0
    total_cost = 0.0
    total_revenue = 0.0
    total_solar_generation = 0.0
    total_load_energy = 0.0

    weekly_power = []
    weekly_load = []
    weekly_net_power = []
    weekly_battery_soc = []
    weekly_grid_import = []
    weekly_grid_export = []
    hourly_time = []
    daily_mean_power = []
    daily_stats = [] 

    print("\nWeekly Microgrid Simulation ")

    for day in range(1, sim_config.DAYS + 1):
        today, tomorrow = simulate_weather(today)
        rain_today, rain_type = simulate_rain(today)
        
        dust_today, manual_cleaning_triggered_today = simulate_dust(dust_today, rain_type)

        day_power = []

        for current_hour in range(sim_config.HOURS_PER_DAY):
            
            is_cleaning_downtime = False
            if cleaning_triggered_yesterday and (sim_config.SUNRISE <= current_hour < sim_config.SUNRISE + 1):
                is_cleaning_downtime = True

            cloud_active = update_cloud_state(cloud_active)
            (
                ideal_power,
                actual_power,
                irradiance,
                soiling_loss,
                temporary_cloud_event
            ) = simulate_solar(
                today,
                dust_today,
                current_hour,
                cloud_active,
                is_cleaning_downtime=is_cleaning_downtime
            )

            load = simulate_load(current_hour)
            net_power = actual_power - load

            if net_power >= 0:
                battery_energy_current, charging_power, grid_export = charge_battery(
                    battery_energy_current, net_power
                )
                grid_import = 0.0
            else:
                battery_energy_current, supplied_power, grid_import = discharge_battery(
                    battery_energy_current, abs(net_power)
                )
                grid_export = 0.0

            total_solar_generation += actual_power
            total_load_energy += load
            total_grid_import += grid_import
            total_grid_export += grid_export
            total_cost += grid_import * sim_config.GRID_BUY_PRICE
            total_revenue += grid_export * sim_config.GRID_SELL_PRICE

            day_power.append(actual_power)
            weekly_power.append(actual_power)
            weekly_load.append(load)
            weekly_net_power.append(net_power)
            weekly_battery_soc.append(battery_energy_current)
            weekly_grid_import.append(grid_import)
            weekly_grid_export.append(grid_export)
            hourly_time.append((day - 1) * sim_config.HOURS_PER_DAY + current_hour)

        mean_power = sum(day_power) / len(day_power)
        daily_mean_power.append(mean_power)

        total_day_solar = sum(day_power)
        total_day_load = sum(weekly_load[-(sim_config.HOURS_PER_DAY):])
        total_day_import = sum(weekly_grid_import[-(sim_config.HOURS_PER_DAY):])
        total_day_export = sum(weekly_grid_export[-(sim_config.HOURS_PER_DAY):])
        
        theoretical_max_day_energy = 522.0 
        solar_efficiency_ratio = (total_day_solar / theoretical_max_day_energy) * 100

        self_sufficiency_index = ((total_day_load - total_day_import) / total_day_load) * 100 if total_day_load > 0 else 0.0

        daily_stats.append({
            "day": day,
            "today_weather": today.name,
            "dust": dust_today,
            "cleaned_today": manual_cleaning_triggered_today,
            "suffered_downtime_today": cleaning_triggered_yesterday,
            "metrics": {
                "solar_generated_kwh": total_day_solar,
                "solar_perf_ratio": min(solar_efficiency_ratio, 100.0),
                "load_consumed_kwh": total_day_load,
                "grid_imported_kwh": total_day_import,
                "grid_exported_kwh": total_day_export,
                "ssi_percentage": self_sufficiency_index,
                "end_of_day_soc_kwh": battery_energy_current
            }
        })

    return {
        "weekly_power": weekly_power,
        "weekly_load": weekly_load,
        "weekly_net_power": weekly_net_power,
        "weekly_battery_soc": weekly_battery_soc,
        "weekly_grid_import": weekly_grid_import,
        "weekly_grid_export": weekly_grid_export,
        "hourly_time": hourly_time,
        "daily_mean_power": daily_mean_power,
        "daily_stats": daily_stats,
        "summary": {
            "solar_gen": total_solar_generation,
            "load_con": total_load_energy,
            "grid_imp": total_grid_import,
            "grid_exp": total_grid_export,
            "final_soc": battery_energy_current,
            "gross_cost": total_cost,
            "gross_rev": total_revenue,
            "net_cost": total_cost - total_revenue
        }
    }