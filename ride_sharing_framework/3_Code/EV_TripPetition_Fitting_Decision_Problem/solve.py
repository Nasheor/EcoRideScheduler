# --------------------------------------------------------
#
# PYTHON PROGRAM DEFINITION
#
# The knowledge a computer has of Python can be specified in 3 levels:
# (1) Prelude knowledge --> The computer has it by default.
# (2) Borrowed knowledge --> The computer gets this knowledge from 3rd party libraries defined by others
#                            (but imported by us in this program).
# (3) Generated knowledge --> The computer gets this knowledge from the new functions defined by us in this program.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer first processes this PYTHON PROGRAM DEFINITION section of the file.
# On it, our computer enhances its Python knowledge from levels (2) and (3) with the imports and new functions
# defined in the program. However, it still does not execute anything.
#
# --------------------------------------------------------

# ------------------------------------------
# IMPORTS
# ------------------------------------------
import solve_TP_2_EV_allocation


def identify_potential_charging_points(EVs, CSs):
    charging_points = {}
    battery_threshold = 30
    for ev_id, ev_data in EVs.items():
        schedule = ev_data[1]
        charging_points[ev_id] = []
        for index, movement in enumerate(schedule):
            battery_level = movement[9]
            if battery_level <= battery_threshold and movement[7] == 0:  # Checking if battery is low and no passengers
                charging_points[ev_id].append(index)
    return charging_points

def evaluate_charging_impact(TPs, EVs, CSs, potential_charging_points, simulation_time):
    charging_impact = {}
    unallocated_tps = []
    station_occupancy = {cs_id: [0]*simulation_time for cs_id in CSs}

    for ev_id, points in potential_charging_points.items():
        charging_impact[ev_id] = {}
        for point in points:
            ev_location = EVs[ev_id][1][point][4:6]  # Getting EV location at the point of potential charging
            nearest_cs, distance_to_cs = find_nearest_charging_station(ev_location, CSs)
            battery_level = EVs[ev_id][1][point][9]
            charging_duration = int((100 - battery_level) / CSs[nearest_cs][4])
            # This is the time the EV will arrive at the Charging station
            time_at_cs = EVs[ev_id][1][point][1] + distance_to_cs
            station_capacity = CSs[nearest_cs][3]
            time_lost = 1000000000
            if time_at_cs < simulation_time:
                if can_charge_at_station(time_at_cs, charging_duration, station_occupancy[nearest_cs][time_at_cs], station_capacity, simulation_time):
                    time_lost = distance_to_cs + charging_duration
                else:
                    time_lost = calculate_wait_time(time_at_cs, charging_duration, station_occupancy[nearest_cs][time_at_cs], station_capacity[nearest_cs])

            # Only consider TPs that the EV could have served after the potential charging start time
            lost_tp_weight = 0
            potential_service_start_time = EVs[ev_id][1][point][1]  # Start time of the movement where EV could have started serving TPs
            for tp_id, tp_info in TPs.items():
                tp_start_time = tp_info[0][0]  # Assuming this is the start time of the TP
                if tp_start_time > potential_service_start_time and tp_start_time <= potential_service_start_time + time_lost:
                    lost_tp_weight += tp_info[0][9]  # TP weight
            charging_impact[ev_id][point] = lost_tp_weight
    return charging_impact

def find_nearest_charging_station(ev_location, CSs):
    nearest_cs = None
    min_distance = float('inf')
    for cs_id, cs_info in CSs.items():
        cs_location = (cs_info[2], cs_info[3])  # Assuming CSs[cs_id] = (cs_id, sec_id, cs_x, cs_y, ...)
        distance = compute_manhattan_distance(ev_location, cs_location)
        if distance < min_distance:
            min_distance = distance
            nearest_cs = cs_id
    return nearest_cs, min_distance

def compute_manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def can_charge_at_station(time_at_cs, charging_duration, occupancy, capacity, simulation_time):
    # Ensure that the CS is available to for the entire Charging duration
    for time_slot in range(time_at_cs, time_at_cs + charging_duration):
        if occupancy >= capacity:
            return False
    return True

def decide_on_charging(EVs, charging_impact):
    acceptable_threshold = 20
    for ev_id, impacts in charging_impact.items():
        best_point = min(impacts, key=impacts.get)  # Choose the point with minimum impact
        if impacts[best_point] < acceptable_threshold:
            EVs[ev_id][1].insert(best_point, create_charging_movement())  # Add charging movement at best_point
    return EVs

def create_charging_movement(start_time, end_time, charging_station_location, EV_initial_battery, EV_max_battery):
    # Assuming the movement format: (start time, end time, start location, end location, initial battery level, final battery level, movement type)
    # Movement type for charging can be a specific integer or string identifier, e.g., 'charge'
    movement_type = 'charge'
    movement = (start_time, end_time, charging_station_location, charging_station_location, EV_initial_battery, EV_max_battery, movement_type)
    return movement

def reallocate_trips_post_charging(EVs, TPs, SECs, unalloated_tps):
    additional_weight = 0
    for tp_id in unallocated_tps:
        for ev_id in EVs.keys():
            # Check if the EV is available after charging
            if EV_is_available_after_charging(EVs[ev_id]):
                allocated = try_to_allocate_EV(tp_id, ev_id, SECs, EVs, TPs)
                if allocated:
                    additional_weight += TPs[tp_id][0][9]  # Add TP weight if allocated
    return additional_weight

def EV_is_available_after_charging(EV, simulation_end_time):
    # Assuming EV's schedule is a list of movements and each movement is a tuple.
    # The end time of the last movement can be used to determine availability.
    last_movement = EV[-1]  # Assuming EV schedule is the last element in EV data structure
    end_time_of_last_movement = last_movement[1]  # Assuming end time is the second element in the movement tuple
    print("Test")
    # Check if the end time of the last movement (charging) is before the simulation end time
    return end_time_of_last_movement < simulation_end_time

def calculate_wait_time(time_at_cs, charging_duration, occupancy, capacity):
    wait_time = 0
    while not can_charge_at_station(time_at_cs + wait_time, charging_duration, occupancy, capacity):
        wait_time += 1
    return wait_time

def try_to_allocate_EV(tp_id, ev_id, SECs, EVs, TPs):
    (my_EV_static_info, my_EV_schedule) = EVs[ev_id]
    max_passengers = my_EV_static_info[3]
    (my_TP_static_info, my_TP_SEC, my_TP_EV) = TPs[tp_id]
    (sec_x_location, sec_y_location, energy_produced) = SECs[my_EV_static_info[0]]
    res = solve_TP_2_EV_allocation.ev_trip_allocation_attempt(my_EV_schedule,
                                                             tp_id,
                                                             my_TP_static_info,
                                                             max_passengers,
                                                             sec_x_location,
                                                             sec_y_location
                                                             )
    return res

# ------------------------------------------
# FUNCTION 01 - reactive_simulation
# ------------------------------------------
def solve_reactive_simulation(city,
                              SECs,
                              CSs,
                              EVs,
                              TPs
                             ):

    res = 0
    sorted_TPs = sorted(TPs.items(), key=lambda tp: (-tp[1][0][9], tp[1][1]))
    EV_IDs = sorted(EVs.keys())
    unallocated_tps = []
    for tp in sorted_TPs:
        tp_id = tp[0]
        is_allocated = False
        for ev_id in EV_IDs:
            # Checking if EV belongs to the community
            tp_sec = TPs[tp_id][1]
            ev_sec = EVs[ev_id][0][0]
            if ev_sec == tp_sec:
                (is_allocated,
                 pick_up_movement_index,
                 drop_off_movement_index,
                 return_to_sec_movement_index,
                 extra_passenger_energy_and_delay_constraints_satisfied,
                 my_new_EV_schedule
                 ) = try_to_allocate_EV(tp_id, ev_id, SECs, EVs, TPs)
                if (is_allocated == True):
                    # I. We update the schedule of the EV
                    EVs[ev_id][1] = my_new_EV_schedule
                    # II. We update the info of TP_allocation
                    TPs[tp_id][2] = ev_id
                    # III. We increase the weight of petitions satisfied
                    res += TPs[tp_id][0][9]
                    # IV. We do not try to allocate it to any other EVs
                    break

            # If unable to satisfy with its own EV, add it to another list
            if ev_id == len(EV_IDs) and is_allocated == False:
                unallocated_tps.append(tp_id)

    for tp_id in unallocated_tps:
        for ev_id in EV_IDs:
            (is_allocated,
             pick_up_movement_index,
             drop_off_movement_index,
             return_to_sec_movement_index,
             extra_passenger_energy_and_delay_constraints_satisfied,
             my_new_EV_schedule
             ) = try_to_allocate_EV(tp_id, ev_id, SECs, EVs, TPs)
        if (is_allocated == True):
            # I. We update the schedule of the EV
            EVs[ev_id][1] = my_new_EV_schedule
            # II. We update the info of TP_allocation
            TPs[tp_id][2] = ev_id
            # III. We increase the weight of petitions satisfied
            res += TPs[tp_id][0][9]
            # IV. We do not try to allocate it to any other EVs
            break


    # Identify potential charging points
    potential_charging_points = identify_potential_charging_points(EVs, CSs)

    # Evaluate charging impact
    simulation_time = city[2]
    charging_impact = evaluate_charging_impact(TPs, EVs, CSs, potential_charging_points, simulation_time)

    # Decide on charging and update EV schedules
    EVs = decide_on_charging(EVs, charging_impact)

    # Reallocate trips post-charging
    additional_weight = reallocate_trips_post_charging(EVs, TPs, SECs, unallocated_tps)

    # Update the simulation result
    res += additional_weight



    # 4. We return res
    return res

