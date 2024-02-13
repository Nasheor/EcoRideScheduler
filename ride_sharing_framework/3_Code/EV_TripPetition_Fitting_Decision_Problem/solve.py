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

def can_charge_at_station(time_at_cs, charging_duration, station_occupancy, capacity):
    # Ensure that the CS is available to for the entire Charging duration
    for time_slot in range(time_at_cs, time_at_cs + charging_duration):
        if station_occupancy[time_slot] >= capacity:
            return False
    return True

def calculate_wait_time(time_at_cs, charging_duration, station_occupancy, capacity):
    wait_time = 0
    while not can_charge_at_station(time_at_cs + wait_time, charging_duration, station_occupancy, capacity):
        wait_time += 1
    return wait_time

def identify_potential_charging_points(EVs, CSs):
    charging_points = {}
    battery_threshold = 40
    for ev_id, ev_data in EVs.items():
        schedule = ev_data[1]
        charging_points[ev_id] = []
        for index, movement in enumerate(schedule):
            battery_level = movement[9]
            # Checking if battery is low and no passengers
            if (battery_level <= battery_threshold and movement[7] == 0 and index != len(schedule)-1):
                charging_points[ev_id].append(index)
            # If the EV has too much leeway time in the final movement, we consider that as a potential charging point
            elif (index == len(schedule)-1 and movement[12] > 40):
                point = index-1
                charging_points[ev_id].append(point)
    return charging_points

def evaluate_charging_impact(TPs, EVs, CSs, potential_charging_points, station_occupancy, simulation_time):
    charging_impact = {}
    # Define weights for each factor
    w1, w2, w3, w4, w5 = 1, 1, 1, 1, 1  # These weights can be adjusted based on their importance

    for ev_id, points in potential_charging_points.items():
        charging_impact[ev_id] = {}
        best_value = float('inf')
        for point in points:
            ev_location = EVs[ev_id][1][point][4:6]
            for cs_id, cs_info in CSs.items():
                cs_location = (cs_info[2], cs_info[3])
                distance_to_cs = compute_manhattan_distance(ev_location, cs_location)
                battery_level = EVs[ev_id][1][point][9]
                charging_duration = int((100 - battery_level) / cs_info[4])
                time_at_cs = EVs[ev_id][1][point][1] + distance_to_cs
                station_capacity = cs_info[3]

                if time_at_cs < simulation_time:
                    simulated_occupancy = station_occupancy.copy()
                    for time_slot in range(time_at_cs, time_at_cs + charging_duration):
                        if time_slot % simulation_time not in simulated_occupancy[cs_id]:
                            simulated_occupancy[cs_id][time_slot % simulation_time] = 1

                    waiting_time = calculate_wait_time(time_at_cs, charging_duration, station_occupancy[cs_id], station_capacity)
                    time_lost = distance_to_cs + charging_duration + waiting_time
                    for other_ev_id, other_ev_schedule in EVs.items():
                        if other_ev_id != ev_id:
                            for movement in other_ev_schedule[1]:
                                if movement[10] == 0 and movement[1] >= time_at_cs:
                                    wait_start = max(time_at_cs, movement[0])
                                    wait_end = min(time_at_cs + charging_duration, movement[1])
                                    waiting_time_other_vehicles += max(0, wait_end - wait_start)

                    # Calculate the potential impact on other vehicles' trip allocations
                    potential_trip_impact = 0
                    for other_ev_id, other_ev_schedule in EVs.items():
                        if other_ev_id != ev_id:
                            for tp_id, tp_info in TPs.items():
                                tp_start_time = tp_info[0][6]
                                tp_late_finish = tp_info[0][8]
                                if tp_start_time >= time_at_cs and tp_late_finish <= time_at_cs + charging_duration:
                                    potential_trip_impact += tp_info[0][9]

                    # Calculate overridden TPs
                    overridden_tps_count = 0
                    unallocated_tps = []
                    for tp_id, tp_info in TPs.items():
                        tp_start_time = tp_info[0][6]
                        tp_late_finish = tp_info[0][8]
                        if tp_start_time > EVs[ev_id][1][point][1] and tp_late_finish <= time_at_cs + time_lost:
                            overridden_tps_count += tp_info[0][9]
                            unallocated_tps.append(tp_id)

                    # How early in the simulation the charging is considered
                    simulation_early_factor = time_at_cs / simulation_time

                    # Calculate the total value considering all factors
                    total_value = (w1 * distance_to_cs) + (w2 * waiting_time) + (w3 * overridden_tps_count) + \
                                  (w4 * simulation_early_factor) + (w5 * potential_trip_impact)
                    if total_value < best_value:
                        best_value = total_value
                        charging_impact[ev_id][(point, cs_id)] =(cs_id, distance_to_cs, waiting_time, charging_duration,
                                                                unallocated_tps )
    return charging_impact


def unpack_charging_movements(EVs, CSs, charging_impact, SECs, simulation_time):
    # Movement type labels as integers
    MOVEMENT_TO_CS = 1001
    MOVEMENT_WAIT_CS = 1002
    MOVEMENT_CHARGE_CS = 1003

    for ev_id, charging_options in charging_impact.items():
        for point, impact in charging_options.items():
            cs_id, distance_to_cs, wait_time, charging_duration, unallocated_tps  = impact
            cs_location = (CSs[cs_id][1], CSs[cs_id][2])
            start_time = EVs[ev_id][1][point[0]][1]  # Assuming the end time of the current movement as the start time for charging
            initial_battery = EVs[ev_id][1][point[0]][9]  # Assuming the ending battery level of the current movement
            end_battery_level = 100
            battery_at_cs = initial_battery - distance_to_cs
            # Insert movements for going to CS, waiting (if necessary), and charging
            EVs[ev_id][1].insert(point[0]+1, create_charging_movement(start_time, start_time + distance_to_cs,
                                                                      cs_location, MOVEMENT_TO_CS, initial_battery, battery_at_cs, distance_to_cs))
            is_waiting = False
            time_finished_charging = start_time + distance_to_cs + wait_time + charging_duration
            if wait_time > 0:
                EVs[ev_id][1].insert(point[0]+2, create_charging_movement(start_time + distance_to_cs, start_time + distance_to_cs + wait_time,
                                                                          cs_location, MOVEMENT_WAIT_CS, initial_battery,
                                                                          battery_at_cs, distance_to_cs))
                is_waiting = True
            if is_waiting:
                EVs[ev_id][1].insert(point[0]+3, create_charging_movement(start_time + distance_to_cs + wait_time,
                                                                          time_finished_charging, cs_location, MOVEMENT_CHARGE_CS,
                                                                          battery_at_cs, end_battery_level, distance_to_cs))

            else:
                if battery_at_cs < 0:
                    battery_at_cs = 0
                EVs[ev_id][1].insert(point[0] + 2, create_charging_movement(start_time + distance_to_cs + wait_time,
                                                                           time_finished_charging,
                                                                            cs_location, MOVEMENT_CHARGE_CS,
                                                                            battery_at_cs, end_battery_level,
                                                                            0))
            # Updating the final two movements of EV according to the charging movement
            penultimate_movement = len(EVs[ev_id][1])-2
            final_movement = len(EVs[ev_id][1])-1
            sec_location = (SECs[EVs[ev_id][0][0]][1], SECs[EVs[ev_id][0][0]][1])
            distance_to_sec = compute_manhattan_distance(cs_location, sec_location)
            # time_at_moment =  EVs[ev_id][1][penultimate_movement][1]
            time_at_moment = simulation_time - distance_to_sec
            leeway = time_at_moment - time_finished_charging
            EVs[ev_id][1][penultimate_movement]= (time_finished_charging, time_at_moment, cs_location[0], cs_location[1],
                                                  cs_location[0], cs_location[1],0,0, end_battery_level, end_battery_level, 0, leeway, 0)
            return_sec = time_at_moment + distance_to_sec
            if distance_to_sec == 0:
                return_sec = EVs[ev_id][1][final_movement][1]
            EVs[ev_id][1][final_movement] = (
            time_at_moment, return_sec, cs_location[0], cs_location[1], sec_location[0],
            sec_location[1],0,0, end_battery_level, (end_battery_level - distance_to_sec), 1000000000, 0, distance_to_sec)

    return EVs

def create_charging_movement(start_time, end_time, location, movement_type, initial_battery, final_battery, movement_distance):
    # Assuming leeway and movement distance are not applicable for charging-related movements
    leeway = 0
    return (start_time, end_time, location[0], location[1], location[0], location[1], 0, 0, initial_battery, final_battery, movement_type, leeway, movement_distance)

def reallocate_trips_post_charging(EVs, TPs, SECs, unallocated_tps, simulation_time):
    additional_weight = 0
    for tp_id in unallocated_tps:
        for ev_id in EVs.keys():
            # Check if the EV is available after charging
            if EV_is_available_after_charging(EVs[ev_id], simulation_time):
                # allocated = try_to_allocate_EV(tp_id, ev_id, SECs, EVs, TPs)
                # if allocated[0]:
                #     additional_weight += TPs[tp_id][0][9]  # Add TP weight if allocated
                #     try:
                #         unallocated_tps.remove(tp_id)
                #     except ValueError:
                #         print(f"{tp_id} is not in the list of unallocated petitions")
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
                    additional_weight += TPs[tp_id][0][9]
                    # IV. We do not try to allocate it to any other EVs
                    try:
                        unallocated_tps.remove(tp_id)
                    except ValueError:
                        print(f"{tp_id} is already allocated and not present in the unallocated list")
                    break
    return additional_weight, EVs

def EV_is_available_after_charging(EV, simulation_end_time):
    # Assuming EV's schedule is a list of movements and each movement is a tuple.
    # The end time of the last movement can be used to determine availability.
    last_movement = EV[-1]  # Assuming EV schedule is the last element in EV data structure
    end_time_of_last_movement = last_movement[-2][1]  # Assuming end time is the second element in the movement tuple
    # Check if the end time of the last movement (charging) is before the simulation end time
    return end_time_of_last_movement <= simulation_end_time


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
    simulation_time = city[2]
    station_occupancy = {cs_id: [0] * simulation_time for cs_id in CSs}
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
    charging_impact = evaluate_charging_impact(TPs, EVs, CSs, potential_charging_points, station_occupancy, simulation_time)

    # Decide on charging and update EV schedules
    EVs = unpack_charging_movements(EVs, CSs, charging_impact, SECs, simulation_time)

    # Reallocate trips post-charging
    times = 5
    for i in range(times):
        additional_weight, EVs = reallocate_trips_post_charging(EVs, TPs, SECs, unallocated_tps, simulation_time)

    # Update the simulation result
    res += additional_weight


    # 4. We return res
    return res, unallocated_tps

