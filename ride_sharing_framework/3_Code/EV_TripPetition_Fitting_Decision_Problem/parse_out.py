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

import codecs
import os.path
import shutil
import pandas as pd

# ------------------------------------------
# FUNCTION 01 - parse_out
# ------------------------------------------
# Description:
# We write the instance_solution to a file
# ----------------------------------------------------
# Input Parameters:
# (1) output_file_name. => The name of the file to write our solution to.
# (2) num_trips_satisfied. => The number of trips satisfied.
# (3) EVs. => The info with the schedule of each EV.
# (4) TPs. => The info regarding each TP.
# ----------------------------------------------------
# Output Parameters:
# ----------------------------------------------------
def parse_out(output_file_name,
              num_trips_satisfied,
              EVs,
              TPs
             ):

    # 1. We open the file for writing
    my_output_stream = codecs.open(output_file_name, "w", encoding="utf-8")

    # 2. We get the ids of the TPs and EVs
    TP_IDs = sorted(TPs.keys())
    EV_IDs = sorted(EVs.keys())

    # 3. We compute the percentage of trips satisfied
    num_trips = len(TP_IDs)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)
    my_str = "TPs satisfied = " + str(num_trips_satisfied) + "; Total TPs = " + str(num_trips) + "; Percentage Satisfied + " + str(round(num_trips_satisfied / num_trips , 3) * 100) + "%\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    # 4. We compute the info per EV
    my_str = "\n-------------------------------------------------------------------------\n\n"
    my_output_stream.write(my_str)
    my_str = "EVs" + "\n\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)
    ev_trips_served = {}
    ev_energy_consumed = {}
    for ev_id in EV_IDs:
        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)
        my_str = "EV" + str(ev_id) + "\n"
        my_output_stream.write(my_str)

        # 4.1. We compute the overall statistics
        TP_served_by_EV = {}
        num_TPs_served = 0
        my_EV_schedule = EVs[ ev_id ][1]
        total_energy = my_EV_schedule[0][8] - my_EV_schedule[-1][9]

        for item in my_EV_schedule:
            if ((item[10] != 0) and (item[10] != 1000000000)):
                if (abs(item[10]) not in TP_served_by_EV):
                    TP_served_by_EV[ abs(item[10]) ] = True
                    num_TPs_served += 1

        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)
        my_str = "Num TPs served = " + str(num_TPs_served) + "\n"
        my_output_stream.write(my_str)
        ev_trips_served[ev_id] = " ".join([ str(x) for x in sorted(TP_served_by_EV.keys()) ])
        # if len(ev_trips_served[ev_id].split(" ")) > 0 and ev_trips_served[ev_id].split(" ")[0]!= '':
        #     trips_served = list(map(int, ev_trips_served[ev_id].split(" ")))
        #     # print(trips_served)
        #     # print(len(trips_served))
        #     ev_x, ev_y = EVs[ev_id][1][0][2], EVs[ev_id][1][0][3]
        #     individual_distance = 0
        #     for trip in trips_served:
        #         trip_pickx, trip_picky = TPs[trip][0][1], TPs[trip][0][2]
        #         trip_dropx, trip_dropy = TPs[trip][0][3], TPs[trip][0][4]
        #         if individual_distance == 0:
        #             individual_distance += calculateManhattanDistance(ev_x, ev_y, trip_pickx, trip_picky)
        #         else:
        #             individual_distance += calculateManhattanDistance(last_dropx, last_dropy, trip_pickx, trip_picky)
        #         individual_distance += calculateManhattanDistance(trip_pickx, trip_picky, trip_dropx, trip_dropy)
        #         last_dropx, last_dropy = trip_dropx, trip_dropy
        my_str = "TPs served = " + ev_trips_served[ev_id] + "\n"
        my_output_stream.write(my_str)
        ev_energy_consumed[ev_id] = total_energy
        my_str = "Total energy used = " + str(total_energy) + "\n"
        my_output_stream.write(my_str)
        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)

        # 4.2. We print the schedule
        my_str = "Schedule:\n"
        my_output_stream.write(my_str)
        for item in my_EV_schedule:
            my_str = " ".join([ str(x) for x in item ]) + "\n"
            my_output_stream.write(my_str)

        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)

    # 5. We compute the info per TP
    my_str = "\n-------------------------------------------------------------------------\n\n"
    my_output_stream.write(my_str)
    my_str = "TPs" + "\n\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    for tp_id in TP_IDs:
        my_str = "\n----------------------\n"
        my_output_stream.write(my_str)
        allocated_to = TPs[tp_id][2]
        if (allocated_to == -1):
            my_str = "TP" + str(tp_id) + " not allocated\n"
        else:
            my_str = "TP" + str(tp_id) + " allocated to " + str(allocated_to) + "\n"
        my_output_stream.write(my_str)
        my_str = "----------------------\n"
        my_output_stream.write(my_str)

    # 6. We close the file
    my_output_stream.close()
    parse_out_analysis(output_file_name,
              num_trips_satisfied,
              EVs,
              TPs,
              ev_trips_served,
              ev_energy_consumed)

def calculateManhattanDistance(pickup_x, pickup_y, drop_x, drop_y):
    return (abs(pickup_x - drop_x) + abs(pickup_y - drop_y))

def parse_out_analysis(output_file_name,
              num_trips_satisfied,
              EVs,
              TPs,
              ev_trips_served,
              ev_energy_consumed
             ):
    outfile = output_file_name.split('/')[4:][1].split('.')[0]+'.xlsx'
    # outfile = output_file_name+'.xlsx'
    analysis_folder = '../../output_analysis/'+output_file_name.split('/')[4:][0]+'/'
    if(os.path.exists(analysis_folder) is False):
        os.mkdir(analysis_folder)
    analysis_file = analysis_folder+outfile
    print('Generating: '+analysis_file)
    EV_IDs = sorted(EVs.keys())
    data_columns = ['Vehicle-ID', 'Petitions' ,'Trips Satisfied','Number of Trips' ,'Sequential Coverage', 'Ride-share Coverage',
                    'Individual Coverage', 'Individual Cars' ]
    data = pd.DataFrame(columns=data_columns)
    for ev_id in EV_IDs:
        if len(ev_trips_served[ev_id].split(" ")) > 0 and ev_trips_served[ev_id].split(" ")[0]!= '':

            # print(ev_trips_served[ev_id])
            # print(len(ev_trips_served[ev_id]))
            trips_served = list(map(int, ev_trips_served[ev_id].split(" ")))
            # print(trips_served)
            # print(len(trips_served))
            ev_x, ev_y = EVs[ev_id][1][0][2], EVs[ev_id][1][0][3]
            sequential_distance = 0
            individual_distance = 0
            for trip in trips_served:
                trip_pickx, trip_picky = TPs[trip][0][1], TPs[trip][0][2]
                trip_dropx, trip_dropy = TPs[trip][0][3], TPs[trip][0][4]
                if sequential_distance == 0:
                    sequential_distance += calculateManhattanDistance(ev_x, ev_y, trip_pickx, trip_picky)
                else:
                    sequential_distance += calculateManhattanDistance(last_dropx, last_dropy, trip_pickx, trip_picky)
                sequential_distance += calculateManhattanDistance(trip_pickx, trip_picky, trip_dropx, trip_dropy)
                individual_distance += (TPs[trip][0][8] - TPs[trip][0][6])
                last_dropx, last_dropy = trip_dropx, trip_dropy
            # Distance travelled before reached home
            tmp_one = EVs[ev_id][1][len(EVs[ev_id][1]) - 1][8]
            # Distance travelled to reach home
            tmp_two = EVs[ev_id][1][len(EVs[ev_id][1]) - 1][9]
            #ev_energy_consumed[ev_id] = 100 - tmp_two
            row = [ev_id, len(TPs), ev_trips_served[ev_id],len(trips_served), sequential_distance,
                   ev_energy_consumed[ev_id], individual_distance, len(trips_served)]
            data.loc[len(data)] = row
        else:
            continue

    data.to_excel(analysis_file, index=False)
