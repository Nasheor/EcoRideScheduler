import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_dummy_data(num_secs, num_css, num_evs, num_tps, battery_capacities):
    """
    Generate dummy data that reflects more realistic effects of battery capacities on trips satisfied.
    """
    # Dummy SEC and CS data
    secs = pd.DataFrame({
        'SEC_id': np.arange(1, num_secs + 1),
        'SEC_x_location': np.random.randint(1, 100, size=num_secs),
        'SEC_y_location': np.random.randint(1, 100, size=num_secs),
        'Energy_Produced': np.random.randint(1000, 5000, size=num_secs),
    })

    # EV data with realistic battery capacity impacts
    evs = pd.DataFrame({
        'EV_id': np.arange(1, num_evs + 1),
        'Battery_capacity': np.random.choice(battery_capacities, num_evs),
    })

    # Modeling a more realistic relationship between battery capacity and trips satisfied
    # Assume each unit of battery capacity can support a fixed number of trips, plus some variance
    base_trips_per_unit_capacity = 0.5  # base number of trips per unit of battery capacity
    evs['Trips_satisfied'] = (evs['Battery_capacity'] * base_trips_per_unit_capacity
                              + np.random.normal(loc=0, scale=2, size=num_evs)).clip(lower=0)  # Add some randomness and ensure no negative values

    return secs, evs

def plot_trips_vs_battery_capacity(evs, folder_name):
    """
    Plot a scatter plot showing the effect of varying battery capacities on trips satisfied.
    """
    fig, ax = plt.subplots()
    sns.scatterplot(data=evs, x='Battery_capacity', y='Trips_satisfied', ax=ax)
    ax.set_title('Effect of Battery Capacity on Trips Satisfied')
    ax.set_xlabel('Battery Capacity (units)')
    ax.set_ylabel('Trips Satisfied')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    plt.savefig(f"{folder_name}/Battery_vs_Trips.png")
    plt.close()

if __name__ == '__main__':
    # Define simulation parameters
    CS_options = [10, 20, 30, 50, 100]
    EV_options = [100, 500]
    TP_options = [2000, 20000, 50000]
    Battery_capacities = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    for cs in CS_options:
        for ev in EV_options:
            for tp in TP_options:
                # Generate data
                secs, evs = generate_dummy_data(cs, cs, ev, tp, Battery_capacities)
                folder_name = f"CS_{cs}_EV_{ev}_TP_{tp}_Analysis"
                # Plot and save the results
                plot_trips_vs_battery_capacity(evs, folder_name)
                print(f"Graphs saved in {folder_name}")
            break
