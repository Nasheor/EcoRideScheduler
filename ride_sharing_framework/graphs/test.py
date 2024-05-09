import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # Sample data (hypothetical results from simulations)
    battery_capacities = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])  # Battery capacity as percentage of 100 units
    trip_satisfaction = np.array([40, 50, 60, 70, 75, 80, 85, 87, 89, 98])  # Percent of trips satisfied

    # Linear graph for battery capacity vs TP satisfied
    # plt.figure(figsize=(10, 6))
    # plt.plot(battery_capacities, trip_satisfaction, marker='o', linestyle='-', color='b')
    # plt.title('Impact of Battery Capacity on Trip Satisfaction')
    # plt.xlabel('Battery Capacity (%)')
    # plt.ylabel('Trip Petitions Satisfied (%)')
    # plt.grid(True)
    # plt.savefig("battery_capacity_vs_trip_satisfaction.png")
    # plt.show()
    # plt.close()

    # average_wait_time = np.array([15, 14, 13, 12, 11, 10, 9, 8, 7, 6])  # Average wait time in minutes
    #
    # fig, ax1 = plt.subplots(figsize=(10, 6))
    #
    # # Plotting trip satisfaction
    # color = 'tab:red'
    # ax1.set_xlabel('Battery Capacity (%)')
    # ax1.set_ylabel('Trip Petitions Satisfied (%)', color=color)
    # ax1.plot(battery_capacities, trip_satisfaction, marker='o', linestyle='-', color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    #
    # # Create a second y-axis for the average wait time
    # ax2 = ax1.twinx()
    # color = 'tab:blue'
    # ax2.set_ylabel('Average Wait Time (minutes)', color=color)
    # ax2.plot(battery_capacities, average_wait_time, marker='s', linestyle='--', color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    #
    # # Adding title and grid
    # plt.title('Impact of Battery Capacity on Trip Satisfaction and Wait Time')
    # ax1.grid(True)
    #
    # # Save the figure
    # plt.savefig("advanced_dual_axis_graph.png")
    # plt.show()

    # average_wait_time = np.array([15, 14, 13, 12, 11, 10, 9, 8, 7, 6])  # Average wait time in minutes
    # energy_consumed = np.array([200, 180, 160, 140, 130, 120, 110, 105, 100, 95])  # Energy consumed in kWh
    #
    # fig, ax1 = plt.subplots(figsize=(10, 6))
    #
    # color = 'tab:red'
    # ax1.set_xlabel('Battery Capacity (%)')
    # ax1.set_ylabel('Trip Petitions Satisfied (%)', color=color)
    # ax1.plot(battery_capacities, trip_satisfaction, marker='o', linestyle='-', color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    #
    # ax2 = ax1.twinx()
    # color = 'tab:blue'
    # ax2.set_ylabel('Average Wait Time (units)', color=color)
    # ax2.plot(battery_capacities, average_wait_time, marker='s', linestyle='--', color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    #
    # # ax3 = ax1.twinx()
    # # ax3.spines["right"].set_position(("axes", 1.2))
    # # color = 'tab:green'
    # # ax3.set_ylabel('Energy Consumed (kWh)', color=color)
    # # ax3.bar(battery_capacities, energy_consumed, color=color, alpha=0.3)
    # # ax3.tick_params(axis='y', labelcolor=color)
    #
    # plt.title('Impact of Battery Capacity on Ride-Sharing Performance')
    # plt.grid(True)
    # plt.savefig("triple_metric_graph.png")
    # plt.show()

    # Sample data # Graph energy availability at a CS vs trips satisfied at a SEC
    # energy_levels = np.array([50, 75, 80, 90, 100])  # Energy cap at each CS in kWh
    # trip_completion = np.array([200, 250, 500, 525, 600])  # Number of trips completed
    # charging_frequency = np.array([30, 25, 20, 15, 10])  # Average charging sessions per day
    # wait_times = np.array([15, 12, 10, 8, 5])  # Average wait time in minutes
    #
    # fig, ax1 = plt.subplots()
    #
    # color = 'tab:red'
    # ax1.set_xlabel('Energy Availability (kWh)')
    # ax1.set_ylabel('Trips Completed', color=color)
    # ax1.plot(energy_levels, trip_completion, marker='o', linestyle='-', color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    #
    # ax2 = ax1.twinx()
    # color = 'tab:blue'
    # ax2.set_ylabel('Charging Frequency', color=color)
    # ax2.plot(energy_levels, charging_frequency, marker='s', linestyle='--', color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    #
    # plt.title('Impact of Energy Availability on Charging Behavior and Trip Completion')
    # plt.grid(True)
    # plt.show()

    # Energy consumed per trip
    # energy_consumed = np.random.normal(loc=50, scale=10, size=100)  # Simulated energy consumption data
    # trips_completed = np.random.normal(loc=200, scale=50, size=100)  # Simulated trips completed data
    #
    # plt.figure(figsize=(10, 6))
    # plt.scatter(energy_consumed, trips_completed, alpha=0.5)
    # plt.title('Energy Consumption vs. Trip Completion')
    # plt.xlabel('Energy Consumed per Trip (units)')
    # plt.ylabel('Trips Completed')
    # plt.grid(True)
    # plt.savefig("energy_vs_trip_completion_scatter.png")
    # plt.show()

    energy_levels = ['Low', 'Medium', 'High']
    wait_times = [15, 10, 5]  # Average wait times in minutes

    plt.figure(figsize=(10, 6))
    plt.bar(energy_levels, wait_times, color=['blue', 'blue', 'blue'])
    plt.title('Wait Times vs. Energy Availability')
    plt.xlabel('Energy Availability')
    plt.ylabel('Average Wait Time (units)')
    plt.savefig("wait_times_vs_energy.png")
    plt.show()

