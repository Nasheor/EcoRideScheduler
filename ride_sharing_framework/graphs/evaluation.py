import matplotlib.pyplot as plt
import numpy as np

# Data for plots
iterations = [3, 5, 10]

# Trip satisfaction data
trip_satisfaction = {
    "GH01": [89.69, 98.66, 98.66],
    "GH02": [51.19, 53.75, 53.75],
    "GH03": [0.06, 0.06, 0.06],
    "NY01": [88.5, 96.5, 96.5]
}

# Charging station energy utilization data
energy_left = {
    "GH01": [5, 2, 2],
    "GH02": [0, 0, 0],
    "GH03": [100, 100, 100],
    "NY01": [8, 6, 4]
}

# Avg. charges data
avg_charges = {
    "GH01": [15, 18, 20],
    "NY01": [35, 45, 50]
}

# Impact of battery capacity on trip satisfaction and charging behavior
battery_capacity = ["100%", "50%", "10%"]
trip_satisfaction_battery = [98.66, 80, 48]
avg_charges_battery = [20, 45, 186]

# Impact of incentives on trip satisfaction
trip_satisfaction_incentives = [98.66, 39.69, 96.5, 53.2]
incentive_labels = ["With Incentives", "Without Incentives (GH01)", "With Incentives (NY01)", "Without Incentives (NY01)"]

# Impact of full charge vs. partial charge
charging_strategies = ["Full Charge", "Half Charge", "50% to 80%"]
trip_satisfaction_charging = {
    "GH01": [98.66, 86.5, 90],
    "NY01": [96.5, 80.8, 88]
}

# Plotting the graphs
plt.figure(figsize=(12, 10))

# Plot 1: Trip Satisfaction Increase with Iterations
plt.subplot(2, 2, 1)
for dataset, values in trip_satisfaction.items():
    plt.plot(iterations, values, label=dataset, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Trip Satisfaction (%)')
plt.title('Trip Satisfaction Increase with Iterations')
plt.legend()
plt.grid(True)

# Plot 2: Charging Station Energy Utilization
plt.subplot(2, 2, 2)
for dataset, values in energy_left.items():
    plt.plot(iterations, values, label=dataset, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Energy Left (%)')
plt.title('Charging Station Energy Utilization')
plt.legend()
plt.grid(True)

# Plot 3: Impact of Battery Capacity on Trip Satisfaction and Charging Behavior
fig, ax1 = plt.subplots(figsize=(6, 4))
ax2 = ax1.twinx()
ax1.bar(battery_capacity, trip_satisfaction_battery, color='g', alpha=0.6, label='Trip Satisfaction')
ax2.plot(battery_capacity, avg_charges_battery, 'b-', marker='o', label='Avg. Charges')

ax1.set_xlabel('Battery Capacity')
ax1.set_ylabel('Trip Satisfaction (%)', color='g')
ax2.set_ylabel('Avg. Charges', color='b')
plt.title('Impact of Battery Capacity on Trip Satisfaction and Charging Behavior')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.grid(True)

# Plot 4: Impact of Incentives on Trip Satisfaction
plt.figure(figsize=(6, 4))
plt.bar(incentive_labels, trip_satisfaction_incentives, color=['blue', 'orange', 'blue', 'orange'])
plt.xlabel('Incentive Type')
plt.ylabel('Trip Satisfaction (%)')
plt.title('Impact of Incentives on Trip Satisfaction')
plt.grid(True)

# Plot 5: Impact of Full Charge vs. Partial Charge
plt.figure(figsize=(6, 4))
index = np.arange(len(charging_strategies))
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, trip_satisfaction_charging["GH01"], bar_width, alpha=opacity, color='r', label='GH01')
rects2 = plt.bar(index + bar_width, trip_satisfaction_charging["NY01"], bar_width, alpha=opacity, color='b', label='NY01')

plt.xlabel('Charging Strategy')
plt.ylabel('Trip Satisfaction (%)')
plt.title('Impact of Full Charge vs. Partial Charge')
plt.xticks(index + bar_width / 2, charging_strategies)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
