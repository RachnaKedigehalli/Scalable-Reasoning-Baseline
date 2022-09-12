#python3 reasoning.py 10

from owlready2 import *
import pandas as pd
import sys
from os import listdir
import time

num_instances = sys.argv[1]

path = "/home/datalake/ReasonAIR/baseline2/"
datafiles_path = path + "datafiles/" + num_instances + "_instances/"

tbox = get_ontology(path + "tbox.owl").load()

def reasoning_on_file(infered, owl_file):
    onto = get_ontology(datafiles_path + owl_file).load()
    with infered:
        sync_reasoner([onto])
    x = infered.get_instances_of(tbox.ElevatorAbnormalTemperatureEvent)
    y = infered.get_instances_of(tbox.ServerRoomTemperatureEvent)

    print('\n' + owl_file + " --> " + str((len(x), len(y))) + '\n')
    return len(x), len(y)

# df = pd.read_csv('info.csv')
start = time.time()

for owl_file in listdir(datafiles_path):
    infered = get_ontology(path + "output" + owl_file +".owl")
    e, s = reasoning_on_file(infered, owl_file)
    # file_name = owl_file[:owl_file.index(".owl")]
    # df.loc[df['Sl.No.'] == int(file_name), 'Inferred_e'] = str(e)
    # df.loc[df['Sl.No.'] == int(file_name), 'Inferred_s'] = str(s)

end = time.time()
print("Time taken: " + str(end-start) + " seconds")
# df.to_csv("info.csv", index=False)
