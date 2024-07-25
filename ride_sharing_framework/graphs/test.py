import matplotlib.pyplot as plt

# Data
iterations = [3, 5, 10]
improvement_gh01 = [8, 10, 10]
improvement_gh02 = [2, 2, 2]
improvement_gh03 = [0, 0, 0]
improvement_ny01 = [2.5, 8, 8]

time_gh01 = [7, 10, 10]
time_gh02 = [7, 10, 12]
time_gh03 = [2, 2, 2]
time_ny01 = [7, 12, 20]

sec_charges = {
    'GH01': (16, 20, 2),
    'GH02': (16, 8, 0),
    'GH03': (1, 0, 100),
    'NY01': (16, 50, 5)
}

battery_capacity = ['100%', '50%', '10%']
trip_satisfaction_battery = [98.66, 85, 48]
avg_charges_battery = [20, 45, 186]

ev_type = ['With Incentives', 'Without Incentives']
trip_satisfaction_incentives = [98.66, 39.69]

charging_strategy = ['Full Charge', 'Half Charge', '50% to 80%']
trip_satisfaction_charging = [98.66, 86.5, 90]

# Plot 1: Trip Satisfaction Increase with Iterations
plt.figure(figsize=(10, 6))
plt.plot(iterations, improvement_gh01, marker='o', color='black', label='GH01')
plt.plot(iterations, improvement_gh02, marker='s', color='red', linestyle='--', label='GH02')
plt.plot(iterations, improvement_gh03, marker='^', color='blue', linestyle=':', label='GH03')
plt.plot(iterations, improvement_ny01, marker='d', color='green', linestyle='-.', label='NY01')
plt.xlabel('Iterations')
plt.ylabel('Improvement (%)')
plt.title('Trip Satisfaction Increase with Iterations')
plt.legend()
plt.grid(True)
plt.savefig('trip_satisfaction_iterations.png')
plt.show()

# Plot 2: Charging Station Usage
labels, avg_charges, energy_left = zip(*sec_charges.values())
plt.figure(figsize=(10, 6))
x = range(len(sec_charges))
plt.bar(x, avg_charges, width=0.4, color='black', label='Avg. Charges', align='center')
plt.bar(x, energy_left, width=0.4, color='gray', label='Energy Left (%)', align='edge')
plt.xlabel('Dataset')
plt.ylabel('Counts/Percentage')
plt.title('Charging Station Usage')
plt.xticks(x, sec_charges.keys())
plt.legend()
plt.grid(True)
plt.savefig('charging_station_usage.png')
plt.show()

# Plot 3: Impact of Battery Capacity on Trip Satisfaction
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'black'
ax1.set_xlabel('Battery Capacity')
ax1.set_ylabel('Trip Satisfaction (%)', color=color)
ax1.bar(battery_capacity, trip_satisfaction_battery, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'red'
ax2.set_ylabel('Avg. Charges', color=color)
ax2.plot(battery_capacity, avg_charges_battery, color=color, marker='o')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Impact of Battery Capacity on Trip Satisfaction')
fig.tight_layout()
plt.savefig('battery_capacity_trip_satisfaction.png')
plt.show()

# Plot 4: Impact of Incentives on Trip Satisfaction
plt.figure(figsize=(10, 6))
plt.bar(ev_type, trip_satisfaction_incentives, color=['black', 'gray'])
plt.xlabel('EV Type')
plt.ylabel('Trip Satisfaction (%)')
plt.title('Impact of Incentives on Trip Satisfaction')
plt.grid(True)
plt.savefig('incentives_impact.png')
plt.show()

# Plot 5: Impact of Charging Strategy on Trip Satisfaction
plt.figure(figsize=(10, 6))
plt.bar(charging_strategy, trip_satisfaction_charging, color=['black', 'gray', 'lightgray'])
plt.xlabel('Charging Strategy')
plt.ylabel('Trip Satisfaction (%)')
plt.title('Impact of Charging Strategy on Trip Satisfaction')
plt.grid(True)
plt.savefig('charging_strategy_impact.png')
plt.show()
