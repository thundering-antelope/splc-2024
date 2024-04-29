from consistency_decision import *
import sys
from timings import Timings

size = int(sys.argv[1])
path_name = "../data"

config_gen_timings = []
realisation_testing_timings = []
consistency_deciding_iterations = []
seeds = []
consistency_deciding_timings = Timings()
sequences = dict()

while len(sequences) < size:
    consistency_deciding_timings.start()
    d = decide_consistency(path_name)

    if d['sequence'] in sequences:
        print('Ignoring reoccured sequence', d['sequence'], 'while collected', consistency_deciding_timings.getLen())
        consistency_deciding_timings.abort()
        continue
    
    consistency_deciding_timings.finish()
    sequences[d['sequence']] = 1
    config_gen_timings.append(d['config_gen_timings'])
    realisation_testing_timings.append(d['realisation_testing_timings'])
    consistency_deciding_iterations.append(d['iterations'])
    seeds.append(d['seed'])

output = []
for i in range(len(consistency_deciding_timings.getList())):
    output.append([
        seeds[i],
        consistency_deciding_iterations[i],
        consistency_deciding_timings.getList()[i],
        (config_gen_timings[i]).getSum(),
        (realisation_testing_timings[i]).getSum()])
write_csv_file(path_name + "/timings.csv", output)
consistency_deciding_timings.print()