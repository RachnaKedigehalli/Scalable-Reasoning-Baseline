# python3 instance_generator.py 10 100
# Folder /datafiles/10_instances should exist
from owlready2 import *
import random
import pandas as pd
import sys

path = "/home/datalake/ReasonAIR/baseline2/"

tbox = get_ontology(path + "tbox.owl").load()

given_instances = sys.argv[1]
num_files = sys.argv[2]

def generate_instances_per_file(tbox, file_num, num_instances):
    for ind in list(tbox.individuals()):
        destroy_entity(ind)
    
    count = 1
    elevator_tmp_event = 0
    serverRoom_tmp_event = 0
    
    with tbox:
        while count <= num_instances:
            # Setting temperature
            temperature = tbox.Temperature("temperature_" + str(file_num) + "_" + str(count))
            
            # location ------
            detector_location = random.choice([0,1])
            if detector_location == 0:
                location = tbox.Elevator("elevator_" + str(file_num) + "_" + str(count))
            # elif detector_location == 1:
            else:
                location = tbox.ServerRoom("server_room_" + str(file_num) + "_" + str(count))
            
            # temperature value
            result = tbox.Result("result_" + str(file_num) + "_" + str(count))
            result_val = random.uniform(20, 120)
            result.hasValue = [result_val]

            observation = tbox.Observation("observation_" + str(file_num) + "_" + str(count))

            observation.observedProperty = [temperature]
            observation.observationResult = [result]
            observation.hasLocation = [location]

            if detector_location == 0 and result_val>40:
                elevator_tmp_event += 1
            if detector_location == 1 and result_val>20:
                serverRoom_tmp_event += 1
            
            count += 1
            # smoke = tbox.Smoke("smoke" + str(now))
    tbox.save(file = path + "datafiles/"+ given_instances +"_instances/" + str(file_num) + ".owl")
    return elevator_tmp_event, serverRoom_tmp_event

def generate_instances(tbox):
    df = pd.DataFrame(columns=['Sl.No.', 'Elevator', 'Server_Room', 'Inferred_e', 'Inferred_s', 'Reasoning_time'])
    # instances = [10, 50, 100, 500]
    num_instances = int(given_instances)
    for i in range(int(num_files)):
        e, s = generate_instances_per_file(tbox, i+1, num_instances)
        df.loc[len(df.index)] = [i+1, e, s, None, None, None]
    df.to_csv("info.csv", index=False)

generate_instances(tbox)
