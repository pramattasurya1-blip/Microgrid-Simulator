# main.py
import matplotlib.pyplot as plt
import numpy as np
import sim_config
from simulation import run_weekly_simulation

def main():
    # 1. Run the core microgrid calculation engine
    results = run_weekly_simulation()

    # Unpack the simulation results dictionary
    weekly_power = results["weekly_power"]
    weekly_load = results["weekly_load"]
    weekly_battery_soc = results["weekly_battery_soc"]
    weekly_grid_import = results["weekly_grid_import"]
    weekly_grid_export = results["weekly_grid_export"]
    hourly_time = results["hourly_time"]
    daily_mean_power = results["daily_mean_power"]
    daily_stats = results["daily_stats"]
    summary = results["summary"]

    # 2. Print Detailed Daily Reports to Console
    for stats in daily_stats:
        m = stats["metrics"]
        
        print(f"\n==================== DAY {stats['day']} SYSTEM LOG ====================")
        print(f" [ENV] Weather Profile    : {stats['today_weather']} | Ending Dust Level: {stats['dust']:.1f}%")
        
        if stats['suffered_downtime_today']:
            print(" [MAINT] MAINTENANCE ALERT: Panels taken OFFLINE for 2 hours this morning.")
        if stats['cleaned_today']:
            print(" [MAINT] MAINTENANCE ALERT: Dust threshold breached. Manual washing triggered for tomorrow.")
            
        print(f" [SOLAR] Performance      : {m['solar_generated_kwh']:.2f} kWh generated  ({m['solar_perf_ratio']:.1f}% Capacity Ratio)")
        print(f" [LOAD] Community Demand  : {m['load_consumed_kwh']:.2f} kWh consumed")
        print(f" [STORAGE] Battery        : Ending State of Charge: {m['end_of_day_soc_kwh']:.2f} kWh")
        print(f" [GRID] Utility Flow      : Imported: {m['grid_imported_kwh']:.2f} kWh | Exported: {m['grid_exported_kwh']:.2f} kWh\n")
        
    
        ssi = m['ssi_percentage']
        print(f" SELF-SUFFICIENCY INDEX (SSI): {ssi:.1f}% of load powered by microgrid assets")
        print("==============================================================")
    # 3. Print Aggregate Weekly Financial & Energy Summary
    print("\n========== Weekly Energy Summary ==========")
    print(f"Total Solar Generation : {summary['solar_gen']:.2f} kWh")
    print(f"Total Load Consumed    : {summary['load_con']:.2f} kWh")
    print(f"Grid Import Volume     : {summary['grid_imp']:.2f} kWh")
    print(f"Grid Export Volume     : {summary['grid_exp']:.2f} kWh")
    print(f"Final Battery SoC      : {summary['final_soc']:.2f} kWh")
    print(f"Gross Grid Import Cost : ₹{summary['gross_cost']:.2f}")
    print(f"Gross Feed-in Revenue  : ₹{summary['gross_rev']:.2f}")
    print(f"Net Electricity Cost   : ₹{summary['net_cost']:.2f}")

    print("\nGenerating Performance Charts.............")

    # Identify best and worst generation days dynamically
    highest_day = np.argmax(daily_mean_power)
    lowest_day = np.argmin(daily_mean_power)
    representative_days = [highest_day, lowest_day]

    fig, ax = plt.subplots(figsize=(12, 5))
    plots = []

    # Plotting solar generation, load, and battery SoC for representative_days
    for day_idx in representative_days:
        def make_plot_day(d):
            return lambda axis: (
                axis.plot(
                    range(sim_config.HOURS_PER_DAY),
                    weekly_power[d * sim_config.HOURS_PER_DAY : (d + 1) * sim_config.HOURS_PER_DAY],
                    label="Solar Generation (kW)", linewidth=2, color="gold"
                ),
                axis.plot(
                    range(sim_config.HOURS_PER_DAY),
                    weekly_load[d * sim_config.HOURS_PER_DAY : (d + 1) * sim_config.HOURS_PER_DAY],
                    label="Complex Load (kW)", linewidth=2, color="crimson"
                ),
                axis.plot(
                    range(sim_config.HOURS_PER_DAY),
                    weekly_battery_soc[d * sim_config.HOURS_PER_DAY : (d + 1) * sim_config.HOURS_PER_DAY],
                    label="Battery SoC (kWh)", linewidth=2, color="teal"
                ),
                axis.set_xlabel("Hour of the Day"),
                axis.set_ylabel("Power (kW) / Energy (kWh)"),
                axis.set_title(
                    f"Representative Day {d + 1} "
                    f"({'HIGHEST' if d == highest_day else 'LOWEST'} Gen Day | Mean = {daily_mean_power[d]:.2f} kW)"
                ),
                axis.grid(True),
                axis.legend()
            )
        plots.append(make_plot_day(day_idx))

    # Plot 3: Daily Mean Solar Trend
    def plot_daily_mean(axis):
        axis.plot(range(1, sim_config.DAYS + 1), daily_mean_power, marker="o", color="orange", linewidth=2)
        axis.set_xlabel("Day")
        axis.set_ylabel("Mean Power (kW)")
        axis.set_title("Daily Mean Solar Generation Trend")
        axis.grid(True)
    plots.append(plot_daily_mean)

    # Plot 4: 7-Day SoC Tracking
    def plot_soc(axis):
        axis.plot(hourly_time, weekly_battery_soc, color="green", linewidth=2)
        axis.set_xlabel("Simulation Hour")
        axis.set_ylabel("Battery Energy (kWh)")
        axis.set_title("7-Day Central Battery Bank State of Charge")
        axis.grid(True)
    plots.append(plot_soc)

    # Plot 5: Grid Exchange Profiles
    def plot_grid(axis):
        axis.plot(hourly_time, weekly_grid_import, label="Grid Import", linewidth=2, color="purple")
        axis.plot(hourly_time, weekly_grid_export, label="Grid Export", linewidth=2, color="navy")
        axis.set_xlabel("Simulation Hour")
        axis.set_ylabel("Power (kW)")
        axis.set_title("Utility Grid Interaction Profile")
        axis.grid(True)
        axis.legend()
    plots.append(plot_grid)

    current_plot = 0
    total_plots = len(plots)

    def draw_plot(index):
        ax.clear()
        plots[index](ax)
        fig.suptitle(f"Plot {index + 1}/{total_plots}    (← Previous | → Next Key)", fontsize=14)
        fig.tight_layout()
        fig.canvas.draw_idle()

    def on_key(event):
        nonlocal current_plot
        if event.key == "right":
            current_plot = (current_plot + 1) % total_plots
        elif event.key == "left":
            current_plot = (current_plot - 1) % total_plots
        else:
            return
        draw_plot(current_plot)

    fig.canvas.mpl_connect("key_press_event", on_key)
    draw_plot(current_plot)
    plt.show()

if __name__ == "__main__":
    main()