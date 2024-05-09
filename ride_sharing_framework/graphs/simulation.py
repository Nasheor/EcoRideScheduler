import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_energy_utilization_as_cheater_plot(energy_levels):
    """
    Plots energy utilization by EVs, with time on the x-axis and EV ID on the y-axis.
    Energy levels are represented by color intensity.
    """
    ev_ids = np.arange(1, energy_levels.shape[0] + 1)
    time_slots = np.arange(energy_levels.shape[1])

    for ev_id in ev_ids:
        plt.scatter(time_slots, [ev_id] * len(time_slots), c=energy_levels.iloc[ev_id - 1], cmap='viridis', marker='s')

    plt.colorbar(label='Energy Level')
    plt.xlabel('Time (Hour)')
    plt.ylabel('EV ID')
    plt.title('Energy Utilization by EVs Over Time')
    plt.show()


def plot_cs_energy_availability_vs_ev_utilization_as_cheater_plot(energy_levels, cs_energy):
    """
    Visualizes CS energy availability versus EV energy utilization over time.
    CS energy availability influences the size of the markers.
    """
    # Assuming cs_energy is a series with the same length as time_slots indicating available energy at each time slot
    time_slots = np.arange(energy_levels.shape[1])
    for i, row in energy_levels.iterrows():
        plt.scatter(time_slots, [i + 1] * len(time_slots), s=cs_energy / 2, c=row, cmap='Blues', alpha=0.5,
                    edgecolor='none')

    plt.colorbar(label='EV Energy Utilization')
    plt.xlabel('Time (Hour)')
    plt.ylabel('EV ID')
    plt.title('CS Energy Availability vs. EV Energy Utilization Over Time')
    plt.show()


def plot_charging_impact_as_cheater_plot(charging_sessions, trip_satisfaction):
    """
    Demonstrates the impact of charging sessions on the number of trips satisfied.
    """
    ev_ids = np.arange(1, charging_sessions.shape[0] + 1)
    total_charges = charging_sessions.sum(axis=1)
    total_trips = trip_satisfaction.sum(axis=1)

    plt.scatter(total_charges, total_trips, c=total_trips, cmap='coolwarm', s=total_charges * 10, alpha=0.6)
    plt.colorbar(label='Total Trips Satisfied')
    plt.xlabel('Total Charges')
    plt.ylabel('Total Trips Satisfied')
    plt.title('Charging Impact vs. Trips Satisfaction')
    plt.show()


def plot_trip_satisfaction_over_time_as_cheater_plot(trip_satisfaction):
    """
    Visualizes trip satisfaction over time using a cheater plot style.
    """
    ev_ids = np.arange(trip_satisfaction.shape[0])
    time_slots = np.arange(trip_satisfaction.shape[1])

    for ev_id in ev_ids:
        plt.scatter(time_slots, [ev_id + 1] * len(time_slots), c=trip_satisfaction.iloc[ev_id], cmap='YlGn', marker='o')

    plt.colorbar(label='Trip Satisfaction')
    plt.xlabel('Time (Hour)')
    plt.ylabel('EV ID')
    plt.title('Trip Satisfaction Over Time')
    plt.show()


def plot_trips_satisfied_vs_charges_as_cheater_plot(trip_satisfaction, charging_sessions):
    """
    Compares the number of trips satisfied with the number of charges using a cheater plot style.
    """
    total_charges = charging_sessions.sum(axis=1)
    total_trips = trip_satisfaction.sum(axis=1)

    plt.scatter(total_charges, total_trips, c=total_trips, cmap='RdYlBu', s=total_charges * 10, alpha=0.6)
    plt.colorbar(label='Total Trips Satisfied')
    plt.xlabel('Total Charges')
    plt.ylabel('Total Trips Satisfied')
    plt.title('Number of Trips Satisfied vs. Number of Charges')
    plt.show()

# Function to generate a carpet plot for energy utilization by EVs
def plot_energy_utilization(energy_levels):
    plt.figure(figsize=(12, 8))
    sns.heatmap(energy_levels, cmap="viridis", cbar_kws={'label': 'Energy Level'})
    plt.title("Energy Utilization by EVs Over Time")
    plt.xlabel("Time (Hour)")
    plt.ylabel("EV ID")
    plt.show()


# Function to generate a carpet plot for CS energy availability vs. energy utilization by EV over time
# For demonstration, let's assume a simplified scenario where CS energy availability is a fixed value over time.
def plot_cs_energy_availability_vs_ev_utilization(energy_levels, cs_energy_availability):
    # Normalize energy levels for visualization
    normalized_energy_levels = energy_levels / energy_levels.max().max()

    plt.figure(figsize=(12, 8))
    sns.heatmap(normalized_energy_levels, cmap="Blues", cbar_kws={'label': 'Normalized Energy Utilization'})
    plt.title("CS Energy Availability vs. Energy Utilization by EVs Over Time")
    plt.xlabel("Time (Hour)")
    plt.ylabel("EV ID")
    plt.axhline(y=cs_energy_availability, color='r', linestyle='--')
    plt.show()


# Function to plot charging impact of EV vs how much trips other EVs could have satisfied if they were chosen to charge
def plot_charging_impact_vs_trips_satisfied(trip_satisfaction, charging_sessions):
    # Simplified demonstration of calculating charging impact
    charging_impact = charging_sessions.sum(axis=1)  # Total number of charges per EV
    trips_satisfied = trip_satisfaction.sum(axis=1)  # Total trips satisfied per EV

    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=charging_impact, y=trips_satisfied)
    plt.title("Charging Impact vs. Number of Trips Satisfied by EVs")
    plt.xlabel("Total Charges")
    plt.ylabel("Total Trips Satisfied")
    plt.show()


# Function to generate a carpet plot for trip satisfaction over time
def plot_trip_satisfaction_over_time(trip_satisfaction):
    plt.figure(figsize=(12, 8))
    sns.heatmap(trip_satisfaction, cmap="YlGn", cbar_kws={'label': 'Trip Satisfaction'})
    plt.title("Trip Satisfaction by EVs Over Time")
    plt.xlabel("Time (Hour)")
    plt.ylabel("EV ID")
    plt.show()


def plot_trip_satisfaction_over_time_as_percentage(trip_satisfaction):
    """
    Visualizes trip satisfaction by EVs over time as a percentage of the maximum trips satisfied at each time slot.
    """
    # Calculate the maximum number of trips satisfied at each time slot
    max_trips_per_slot = trip_satisfaction.max(axis=0)

    # Calculate the percentage of the max trips satisfied by each EV at each time slot
    trip_satisfaction_percentage = (trip_satisfaction / max_trips_per_slot) * 100

    plt.figure(figsize=(12, 8))
    sns.heatmap(trip_satisfaction_percentage, cmap="YlGn", cbar_kws={'label': 'Trip Satisfaction (%)'})
    plt.title("Trip Satisfaction by EVs Over Time (as % of Max Possible)")
    plt.xlabel("Time (Hour)")
    plt.ylabel("EV ID")
    plt.show()
# Function to plot number of trips satisfied vs number of charges
def plot_trips_satisfied_vs_charges(trip_satisfaction, charging_sessions):
    trips_satisfied = trip_satisfaction.sum(axis=1)  # Total trips satisfied per EV
    total_charges = charging_sessions.sum(axis=1)  # Total number of charges per EV

    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=total_charges, y=trips_satisfied)
    plt.title("Number of Trips Satisfied vs. Number of Charges")
    plt.xlabel("Total Number of Charges")
    plt.ylabel("Total Number of Trips Satisfied")
    plt.show()
def generate_dummy_data(num_secs, num_css, num_evs, num_tps, simulation_time_horizon, city_max_x_location, city_max_y_location):
    # Generating SECs information
    secs = pd.DataFrame({
        'SEC_id': np.arange(1, num_secs + 1),
        'SEC_x_location': np.random.randint(1, city_max_x_location, size=num_secs),
        'SEC_y_location': np.random.randint(1, city_max_y_location, size=num_secs),
        'Energy_Produced': np.random.randint(1000, 5000, size=num_secs),
    })

    # Generating Charging Stations information
    css = pd.DataFrame({
        'CS_id': np.arange(1, num_css + 1),
        'SEC_id': np.random.choice(secs['SEC_id'], num_css),
        'CS_x_location': np.random.randint(1, city_max_x_location, size=num_css),
        'CS_y_location': np.random.randint(1, city_max_y_location, size=num_css),
        'Queue_Limit': np.random.randint(1, 10, size=num_css),
        'Charging_released_per_unit_time': np.random.randint(10, 50, size=num_css),
    })

    # Generating EVs information
    evs = pd.DataFrame({
        'EV_id': np.arange(1, num_evs + 1),
        'SEC_id': np.random.choice(secs['SEC_id'], num_evs),
        'EV_release_time': np.random.randint(0, simulation_time_horizon, size=num_evs),
        'EV_battery_energy': np.random.randint(20, 100, size=num_evs),  # Initial battery level
        'EV_max_passengers': np.random.randint(1, 5, size=num_evs),
    })

    # Generating TPs information
    tps = pd.DataFrame({
        'Tp_Id': np.arange(1, num_tps + 1),
        'SEC_Id': np.random.choice(secs['SEC_id'], num_tps),
        'EV_id': np.random.choice(evs['EV_id'], num_tps),
        'SX': np.random.randint(1, city_max_x_location, size=num_tps),
        'SY': np.random.randint(1, city_max_y_location, size=num_tps),
        'TX': np.random.randint(1, city_max_x_location, size=num_tps),
        'TY': np.random.randint(1, city_max_y_location, size=num_tps),
        'EP': np.random.randint(0, simulation_time_horizon, size=num_tps),  # Early pick-up
        'LP': np.random.randint(0, simulation_time_horizon, size=num_tps),  # Late pick-up
        'ED': np.random.randint(0, simulation_time_horizon, size=num_tps),  # Early drop-off
        'UB': np.random.randint(0, simulation_time_horizon, size=num_tps),  # Late drop-off
        'TW': np.random.randint(1, 10, size=num_tps),  # Weight of the trip petition
    })

    return secs, css, evs, tps
if __name__ == '__main__':
    # Parameters for data generation
    num_secs = 50
    num_css = 50
    num_evs = 500
    num_tps = 50000
    simulation_time_horizon = 1440
    city_max_x_location = 1000
    city_max_y_location = 1000

    # secs, css, evs, tps = generate_dummy_data(num_secs, num_css, num_evs, num_tps, simulation_time_horizon,
    #                                           city_max_x_location, city_max_y_location)

    # Simulate data generation parameters
    num_evs = 500
    simulation_time_horizon = 24  # Assuming each unit is an hour for simplicity

    # Initialize data structures
    energy_levels = pd.DataFrame(np.random.randint(30, 500, size=(num_evs, simulation_time_horizon)))
    charging_sessions = pd.DataFrame(0, index=np.arange(num_evs), columns=np.arange(simulation_time_horizon))
    trip_satisfaction = pd.DataFrame(0, index=np.arange(num_evs), columns=np.arange(simulation_time_horizon))

    # Simulate changes in energy level (dummy logic for illustrative purposes)
    for ev in range(num_evs):
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
    for ev in range(num_evs):
        for hour in range(simulation_time_horizon):
            # Assume trips can be satisfied if energy is above a threshold and not charging
            if energy_levels.iloc[ev, hour] > 25 and charging_sessions.iloc[ev, hour] == 0:
                trip_satisfaction.iloc[ev, hour] = np.random.randint(1, 4)  # Random number of trips satisfied

    # Convert simulated data to a suitable format for visualization
    # For instance, you can reshape data or calculate additional metrics as needed for the plots

    # Example data ready for visualization
    print("Energy Levels (Sample):")
    print(energy_levels.head())
    print("\nCharging Sessions (Sample):")
    print(charging_sessions.head())
    print("\nTrip Satisfaction (Sample):")
    print(trip_satisfaction.head())
    cs_energy_availability = 100

    # Generate the plots
    plot_energy_utilization(energy_levels)
    plot_cs_energy_availability_vs_ev_utilization(energy_levels, cs_energy_availability)
    plot_charging_impact_vs_trips_satisfied(trip_satisfaction, charging_sessions)
    plot_trip_satisfaction_over_time(trip_satisfaction)
    plot_trip_satisfaction_over_time_as_percentage(trip_satisfaction)
    plot_trips_satisfied_vs_charges(trip_satisfaction, charging_sessions)

    # Using the cheater plot style functions
    plot_energy_utilization_as_cheater_plot(energy_levels)
    plot_cs_energy_availability_vs_ev_utilization_as_cheater_plot(energy_levels, cs_energy_availability)
    plot_charging_impact_as_cheater_plot(charging_sessions, trip_satisfaction)
    plot_trip_satisfaction_over_time_as_cheater_plot(trip_satisfaction)
    plot_trips_satisfied_vs_charges_as_cheater_plot(trip_satisfaction, charging_sessions)