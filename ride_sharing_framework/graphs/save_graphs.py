import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Ensure the plotting functions do not call plt.show() but instead save the plots to files
def save_plot(figure, folder_name, file_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    figure.savefig(f"{folder_name}/{file_name}")
    plt.close()


# Modify each plotting function to save plots instead of showing them immediately
# Example modification for one plotting function:
def plot_energy_utilization_as_cheater_plot(energy_levels, folder_name):
    ev_ids = np.arange(1, energy_levels.shape[0] + 1)
    time_slots = np.arange(energy_levels.shape[1])
    fig, ax = plt.subplots()
    for ev_id in ev_ids:
        ax.scatter(time_slots, [ev_id] * len(time_slots), c=energy_levels.iloc[ev_id - 1], cmap='viridis', marker='s')
    plt.colorbar(label='Energy Level', ax=ax)
    plt.xlabel('Time (Hour)')
    plt.ylabel('EV ID')
    plt.title('Energy Utilization by EVs Over Time')
    save_plot(fig, folder_name, 'Energy_Utilization.png')


def plot_energy_utilization_as_cheater_plot(energy_levels, folder_name):
    """
    Plots energy utilization by EVs, with time on the x-axis and EV ID on the y-axis.
    Energy levels are represented by color intensity.
    """
    ev_ids = np.arange(1, energy_levels.shape[0] + 1)
    time_slots = np.arange(energy_levels.shape[1])
    fig, ax = plt.subplots()
    for ev_id in ev_ids:
        plt.scatter(time_slots, [ev_id] * len(time_slots), c=energy_levels.iloc[ev_id - 1], cmap='viridis', marker='s')

    plt.colorbar(label='Energy Level')
    plt.xlabel('Time (Hour)')
    plt.ylabel('EV ID')
    plt.title('Energy Utilization by EVs Over Time')
    save_plot(fig, folder_name, 'Energy_Utilization_cheater_plot.png')


def plot_cs_energy_availability_vs_ev_utilization_as_cheater_plot(energy_levels, cs_energy, folder_name):
    """
    Visualizes CS energy availability versus EV energy utilization over time.
    CS energy availability influences the size of the markers.
    """
    # Assuming cs_energy is a series with the same length as time_slots indicating available energy at each time slot
    time_slots = np.arange(energy_levels.shape[1])
    fig, ax = plt.subplots()
    for i, row in energy_levels.iterrows():
        plt.scatter(time_slots, [i + 1] * len(time_slots), s=cs_energy / 2, c=row, cmap='Blues', alpha=0.5,
                    edgecolor='none')

    plt.colorbar(label='EV Energy Utilization')
    plt.xlabel('Time (Hour)')
    plt.ylabel('EV ID')
    plt.title('CS Energy Availability vs. EV Energy Utilization Over Time')
    save_plot(fig, folder_name, 'Energy_availability.png')


def plot_charging_impact_as_cheater_plot(charging_sessions, trip_satisfaction, folder_name):
    """
    Demonstrates the impact of charging sessions on the number of trips satisfied.
    """
    ev_ids = np.arange(1, charging_sessions.shape[0] + 1)
    total_charges = charging_sessions.sum(axis=1)
    total_trips = trip_satisfaction.sum(axis=1)
    fig, ax = plt.subplots()

    plt.scatter(total_charges, total_trips, c=total_trips, cmap='coolwarm', s=total_charges * 10, alpha=0.6)
    plt.colorbar(label='Total Trips Satisfied')
    plt.xlabel('Total Charges')
    plt.ylabel('Total Trips Satisfied')
    plt.title('Charging Impact vs. Trips Satisfaction')
    save_plot(fig, folder_name, 'Charging_impact.png')


def plot_trip_satisfaction_over_time_as_cheater_plot(trip_satisfaction, folder_name):
    """
    Visualizes trip satisfaction over time using a cheater plot style.
    """
    ev_ids = np.arange(trip_satisfaction.shape[0])
    time_slots = np.arange(trip_satisfaction.shape[1])
    fig, ax = plt.subplots()
    for ev_id in ev_ids:
        plt.scatter(time_slots, [ev_id + 1] * len(time_slots), c=trip_satisfaction.iloc[ev_id], cmap='YlGn', marker='o')

    plt.colorbar(label='Trip Satisfaction')
    plt.xlabel('Time (Hour)')
    plt.ylabel('EV ID')
    plt.title('Trip Satisfaction Over Time')
    save_plot(fig, folder_name, 'Trip_satisfaction.png')


def plot_trips_satisfied_vs_charges_as_cheater_plot(trip_satisfaction, charging_sessions, folder_name):
    """
    Compares the number of trips satisfied with the number of charges using a cheater plot style.
    """
    total_charges = charging_sessions.sum(axis=1)
    total_trips = trip_satisfaction.sum(axis=1)
    fig, ax = plt.subplots()
    plt.scatter(total_charges, total_trips, c=total_trips, cmap='RdYlBu', s=total_charges * 10, alpha=0.6)
    plt.colorbar(label='Total Trips Satisfied')
    plt.xlabel('Total Charges')
    plt.ylabel('Total Trips Satisfied')
    plt.title('Number of Trips Satisfied vs. Number of Charges')
    save_plot(fig, folder_name, 'Trips_satisfied_vs_charges.png')

# Function to generate a carpet plot for energy utilization by EVs
def plot_energy_utilization(energy_levels, folder_name):
    plt.figure(figsize=(12, 8))
    fig, ax = plt.subplots()
    sns.heatmap(energy_levels, cmap="viridis", cbar_kws={'label': 'Energy Level'})
    plt.title("Energy Utilization by EVs Over Time")
    plt.xlabel("Time (Hour)")
    plt.ylabel("EV ID")
    save_plot(fig, folder_name, 'Simple_energy_usage.png')


# Function to generate a carpet plot for CS energy availability vs. energy utilization by EV over time
# For demonstration, let's assume a simplified scenario where CS energy availability is a fixed value over time.
def plot_cs_energy_availability_vs_ev_utilization(energy_levels, cs_energy_availability, folder_name):
    # Normalize energy levels for visualization
    normalized_energy_levels = energy_levels / energy_levels.max().max()
    fig, ax = plt.subplots()
    plt.figure(figsize=(12, 8))
    sns.heatmap(normalized_energy_levels, cmap="Blues", cbar_kws={'label': 'Normalized Energy Utilization'})
    plt.title("CS Energy Availability vs. Energy Utilization by EVs Over Time")
    plt.xlabel("Time (Hour)")
    plt.ylabel("EV ID")
    plt.axhline(y=cs_energy_availability, color='r', linestyle='--')
    save_plot(fig, folder_name, 'Energy_Avail_ev_utilize.png')


# Function to plot charging impact of EV vs how much trips other EVs could have satisfied if they were chosen to charge
def plot_charging_impact_vs_trips_satisfied(trip_satisfaction, charging_sessions, folder_name):
    # Simplified demonstration of calculating charging impact
    charging_impact = charging_sessions.sum(axis=1)  # Total number of charges per EV
    trips_satisfied = trip_satisfaction.sum(axis=1)  # Total trips satisfied per EV
    fig, ax = plt.subplots()
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=charging_impact, y=trips_satisfied)
    plt.title("Charging Impact vs. Number of Trips Satisfied by EVs")
    plt.xlabel("Total Charges")
    plt.ylabel("Total Trips Satisfied")
    save_plot(fig, folder_name, 'charging_impact_vs_trips_satisfied.png')


# Function to generate a carpet plot for trip satisfaction over time
def plot_trip_satisfaction_over_time(trip_satisfaction, folder_name):
    plt.figure(figsize=(12, 8))
    fig, ax = plt.subplots()
    sns.heatmap(trip_satisfaction, cmap="YlGn", cbar_kws={'label': 'Trip Satisfaction'})
    plt.title("Trip Satisfaction by EVs Over Time")
    plt.xlabel("Time (Hour)")
    plt.ylabel("EV ID")
    save_plot(fig, folder_name, 'trip_satisfaction_over_time.png')


def plot_trip_satisfaction_over_time_as_percentage(trip_satisfaction, folder_name):
    """
    Visualizes trip satisfaction by EVs over time as a percentage of the maximum trips satisfied at each time slot.
    """
    # Calculate the maximum number of trips satisfied at each time slot
    max_trips_per_slot = trip_satisfaction.max(axis=0)
    fig, ax = plt.subplots()
    # Calculate the percentage of the max trips satisfied by each EV at each time slot
    trip_satisfaction_percentage = (trip_satisfaction / max_trips_per_slot) * 100

    plt.figure(figsize=(12, 8))
    sns.heatmap(trip_satisfaction_percentage, cmap="YlGn", cbar_kws={'label': 'Trip Satisfaction (%)'})
    plt.title("Trip Satisfaction by EVs Over Time (as % of Max Possible)")
    plt.xlabel("Time (Hour)")
    plt.ylabel("EV ID")
    save_plot(fig, folder_name, 'trip_satisfaction_over_time_as_percentage.png')


# Function to plot number of trips satisfied vs number of charges
def plot_trips_satisfied_vs_charges(trip_satisfaction, charging_sessions, folder_name):
    trips_satisfied = trip_satisfaction.sum(axis=1)  # Total trips satisfied per EV
    total_charges = charging_sessions.sum(axis=1)  # Total number of charges per EV
    fig, ax = plt.subplots()
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=total_charges, y=trips_satisfied)
    plt.title("Number of Trips Satisfied vs. Number of Charges")
    plt.xlabel("Total Number of Charges")
    plt.ylabel("Total Number of Trips Satisfied")
    save_plot(fig, folder_name, 'trips_satisfied_vs_charg.png')

# Dummy data generation function (simplified example, adjust as needed)
def generate_dummy_data(num_secs, num_css, ev_count, num_tps):
    # Dummy data generation logic here
    return pd.DataFrame(np.random.rand(ev_count, 24) * 100)  # Simplified example


if __name__ == '__main__':
    CS_options = [10, 20, 30, 50, 100]
    EV_options = [100, 500]
    TP_options = [50000]

    for cs_count in CS_options:
        for ev_count in EV_options:
            for tp_count in TP_options:
                # Generate dummy data for this combination
                energy_levels = generate_dummy_data(cs_count, ev_count, ev_count, tp_count)

                # Define folder name for this combination
                folder_name = f"CS_{cs_count}_EV_{ev_count}_TP_{tp_count}"


                simulation_time_horizon = 24  # Assuming each unit is an hour for simplicity

                # Initialize data structures
                energy_levels = pd.DataFrame(np.random.randint(30, 500, size=(ev_count, simulation_time_horizon)))
                charging_sessions = pd.DataFrame(0, index=np.arange(ev_count),
                                                 columns=np.arange(simulation_time_horizon))
                trip_satisfaction = pd.DataFrame(0, index=np.arange(ev_count),
                                                 columns=np.arange(simulation_time_horizon))

                # Simulate changes in energy level (dummy logic for illustrative purposes)
                for ev in range(ev_count):
                    for hour in range(1, simulation_time_horizon):
                        # Simulate energy consumption
                        energy_consumed = np.random.randint(1, 5)
                        energy_levels.iloc[ev, hour] -= energy_consumed

                        # Randomly simulate charging sessions
                        if np.random.rand() > 0.8:  # Assume 20% chance of charging every hour
                            charging_sessions.iloc[ev, hour] = 1  # Mark this hour as a charging session
                            energy_levels.iloc[ev, hour] += np.random.randint(5, 20)  # Simulate charging

                        # Ensure energy levels are within bounds
                        energy_levels.iloc[ev, hour] = min(max(energy_levels.iloc[ev, hour], 0), 100)

                # Simulate trip satisfaction (again, dummy logic for illustrative purposes)
                for ev in range(ev_count):
                    for hour in range(simulation_time_horizon):
                        # Assume trips can be satisfied if energy is above a threshold and not charging
                        if energy_levels.iloc[ev, hour] > 25 and charging_sessions.iloc[ev, hour] == 0:
                            trip_satisfaction.iloc[ev, hour] = np.random.randint(1,
                                                                                 4)  # Random number of trips satisfied

                cs_energy_availability = 100

                # Plot and save graphs for this combination
                plot_energy_utilization_as_cheater_plot(energy_levels, folder_name)
                # Call other plotting functions here, each saving its output to `folder_name`
                plot_energy_utilization(energy_levels, folder_name)
                plot_cs_energy_availability_vs_ev_utilization(energy_levels, cs_energy_availability, folder_name)
                plot_charging_impact_vs_trips_satisfied(trip_satisfaction, charging_sessions, folder_name)
                plot_trip_satisfaction_over_time(trip_satisfaction, folder_name)
                plot_trip_satisfaction_over_time_as_percentage(trip_satisfaction, folder_name)
                plot_trips_satisfied_vs_charges(trip_satisfaction, charging_sessions, folder_name)

                # Using the cheater plot style functions
                plot_energy_utilization_as_cheater_plot(energy_levels, folder_name)
                plot_cs_energy_availability_vs_ev_utilization_as_cheater_plot(energy_levels, cs_energy_availability, folder_name)
                plot_charging_impact_as_cheater_plot(charging_sessions, trip_satisfaction, folder_name)
                plot_trip_satisfaction_over_time_as_cheater_plot(trip_satisfaction, folder_name)
                plot_trips_satisfied_vs_charges_as_cheater_plot(trip_satisfaction, charging_sessions, folder_name)

                print(f"Graphs saved for CS: {cs_count}, EV: {ev_count}, TP: {tp_count}")