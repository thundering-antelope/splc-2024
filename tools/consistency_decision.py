from z3 import *
from config_utils import *
from file_utils import *
from realisation_test import *
import config_utils as config_utils
from timings import Timings

def decide_consistency(path_name):

    # resource types
    Rt = get_resource_types(path_name)

    # resource prov
    Rp = get_resource_provisions(path_name)

    # fm
    features, cnf = read_dimacs_featuremodel(path_name) # -> ([](name, z3_value), cnf)

    # create dict feature-name -> (id, z3_variable, demands=[])
    fd = dict()
    for idx, feature in enumerate(features):
        feature_name, z3_feature = feature
        fd[feature_name] = (idx, z3_feature, [])

    # insert demands into dict entries
    fd, max_i, max_k = read_xml_feature_demands(path_name, fd)
    I = max_i + 1
    K = max_k + 1
    assert(len(Rt) == K)

    # collect feature resource demands
    Frd = [[[] for _ in range(K)] for _ in range(I)]
    for (feature_name, (_, z3_feature, demands)) in fd.items():
        for i, k, v in demands:
            Frd[i][k].append((z3_feature, v, feature_name))

    config_gen_timings = Timings()
    realisation_testing_timings = Timings()

    valid_config_generator = ValidConfigGen(cnf, features)
    config_gen_timings.start()
    config = valid_config_generator.next()

    config_gen_timings.finish()
    config = valid_config_generator.next()
    
    iterations = 0
    while config != None:
        
        iterations += 1

        def red(array, rt):
            nil = -1

            # restrict array to demands of selected features
            def is_selected(feature_name):
                return config[fd[feature_name][0]][1]
            
            array = [demand for _, demand, feature_name in array if is_selected(feature_name)]
            if len(array) == 0: return nil
            elif rt[0] == 0:
                if rt[2] == 0: return max(array)
                elif rt[2] == 1: return min(array)
                else:
                    return array[1]
            else:
                return sum(array)
        
        # resource demand constraints: reduced feature resource demands
        Rd = [[-1 for k in range(K)] for i in range(I)]
        for i in range(I):
            for k in range(K):
                Rd[i][k] = red(Frd[i][k], Rt[k])
        
        realisation_tester = RealisationTester(path_name, Rt, Rp, Rd)
        
        realisation_testing_timings.start()
        result = realisation_tester.solve()
        realisation_testing_timings.finish()

        if result:
            config_gen_timings.start()
            config = valid_config_generator.next()
            config_gen_timings.finish()
        else:
            break

    return {
        'config_gen_timings':config_gen_timings,
        'realisation_testing_timings':realisation_testing_timings,
        'iterations':iterations,
        'seed':valid_config_generator.seed,
        'sequence':valid_config_generator.sequence
    }