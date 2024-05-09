import numpy as np
import matplotlib.pyplot as plt

' Analyze how charging decisions vary based on proximity to charging infrastructure. Evaluate the ' \
'distribution of charging points and identify trends such as clustering around charging stations with shorter distances. ' \
'Highlight the importance of minimizing distance to optimize charging efficiency.'
def distance_to_cs():
    # Generate dummy data
    num_points = 50
    distances = np.random.randint(1, 200, num_points)  # Random distances from 1 to 20

    # Create histogram
    plt.hist(distances, bins=10, color='skyblue', edgecolor='black')
    plt.title('Distribution of Charging Point Distances from CS')
    plt.xlabel('Distance from CS')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


'Examine the waiting times experienced by EVs at charging stations and assess their impact on charging decisions.'
'Discuss factors influencing waiting times, such as station capacity and demand fluctuations. ' \
'Emphasize the need to minimize waiting times to enhance system efficiency and user satisfaction.'
def waiting_time_cs():
    # Generate dummy data
    num_ev = 1000
    waiting_times = np.random.randint(0, 8, num_ev)  # Random waiting times from 0 to 30 minutes

    # Create histogram
    plt.hist(waiting_times, bins=10, color='lightgreen', edgecolor='black')
    plt.title('Distribution of Waiting Times at CS')
    plt.xlabel('Waiting Time')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

'Evaluate the frequency and extent of trip disruptions caused by charging decisions. ' \
'Discuss the implications of overridden trip petitions on trip fulfillment and user experience. Highlight the importance ' \
'of minimizing conflicts between charging requirements and trip schedules to optimize system performance.'
def overriden_tp_count():
    # Generate dummy data
    num_ev = 1000
    overridden_trips = np.random.randint(0,100, num_ev)  # Random overridden trip counts

    # Create bar chart
    plt.bar(range(num_ev), overridden_trips, color='orange', edgecolor='black')
    plt.title('Overridden Trip Count due to Charging Events')
    plt.xlabel('EV Index')
    plt.ylabel('Overridden Trip Count')
    plt.grid(axis='y')
    plt.show()


'Analyze the timing of charging events relative to the simulation timeline. Discuss trends such as peak charging periods' \
' and variations in charging activity throughout the simulation. Assess the impact of charging timing on system resource ' \
'utilization and scheduling flexibility.'
def timing_of_charging_sim():
    # Generate dummy data
    num_charging_events = 1000
    charging_timestamps = np.sort(np.random.randint(0, 1440,
                                                    num_charging_events))  # Random timestamps in minutes (assuming a 24-hour simulation period)

    # Create line chart
    plt.plot(charging_timestamps, np.arange(num_charging_events), color='red', marker='o')
    plt.title('Timing of Charging Events in Simulation')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Charging Event Count')
    plt.grid(True)
    plt.show()

'Examine how charging decisions affect the availability and utilization of charging stations for neighboring EVs. ' \
'Discuss patterns of resource sharing and congestion at charging stations. Evaluate strategies to optimize charging ' \
'resource allocation and mitigate potential conflicts among EVs.'
def  impact_on_other_ev():
    # Generate dummy data
    num_ev = 1000
    num_time_slots = 1440  # Assuming a simulation period of 24 hours with 1-minute time slots
    charging_utilization = np.random.rand(num_ev, num_time_slots)  # Random utilization values between 0 and 1

    # Create heatmap
    plt.imshow(charging_utilization, cmap='hot', aspect='auto', origin='lower')
    plt.colorbar(label='Utilization')
    plt.title('Charging Station Utilization by EVs over Time')
    plt.xlabel('Time Slot')
    plt.ylabel('EV Index')
    plt.show()


if __name__ == '__main__':
    distance_to_cs()
    waiting_time_cs()
    overriden_tp_count()
    timing_of_charging_sim()
    impact_on_other_ev()