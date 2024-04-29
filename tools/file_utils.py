from xml.dom.minidom import parse
from z3 import And, Or, Not, Bool
import csv, os

def read_dimacs_featuremodel(path_name):
    atoms = [] # raw feature variables
    terms = [] # dimacs cnf lines
    with open(path_name + '/model.dimacs') as file:
        for line in file:
            tokens = line.split(' ')
            if tokens[0] == '0': # EOF
                break
            if tokens[0] == 'c': # c id featurename
                atoms.append((int(tokens[1]), tokens[2][:-1]))
            elif tokens[0] == 'p': # p cnf atoms terms
                pass
            else: # cnf line
                terms.append([int(atom_pos) for atom_pos in tokens[:-1]])
    
    # write (feature-name, z3-variable) into 'features' list
    features = [('', None)]*len(atoms)
    for pos, name in atoms: features[pos - 1] = (name, Bool(name))

    # generate cnf from dimacs terms
    def decide_term_id(id):
        if id > 0: return features[id - 1][1]
        else: return Not(features[abs(id) - 1][1])
    cnf = And([ Or([decide_term_id(id) for id in term]) for term in terms])

    return (features, cnf)

def _read_xml_dom(path_name):
    with open(path_name) as file:
        document = parse(file)
    return document

def read_xml_feature_demands(path_name, fd):
    max_i = 0
    max_k = 0
    struct = _read_xml_dom(path_name + '/model.xml').getElementsByTagName('struct')[0]

    # iterate over all 'attribute' tags in xml dom
    for attribute in struct.getElementsByTagName('attribute'):
        feature_name = attribute.parentNode.getAttribute('name')
        tokens = attribute.getAttribute('name')[1:-1].split(',')
        i = int(tokens[0])
        k = int(tokens[1])
        max_i = max(max_i, i)
        max_k = max(max_k, k)
        v = int(attribute.getAttribute('value'))

        # write demands for feature into fd
        if feature_name in fd:
            fd[feature_name][2].append((i, k, v))
    
    return (fd, max_i, max_k)

def _read_csv_file(file_name, conversion = None, hasRowHeader = False, hasColumnHeader = False):
	if conversion == None:
		conversion = lambda v: v
	with open(file_name) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		if hasColumnHeader: next(reader)
		return [[conversion(row[i]) for i in range(hasRowHeader, len(row))] for row in reader if row]		

def _read_csv_resource_file(file_name, hasRowHeader = False):
	return _read_csv_file(file_name, lambda v: -1 if v == '' else int(v), hasRowHeader, False)

def get_resource_types(path_name): return _read_csv_resource_file(path_name + '/resource_types.csv', True)
def get_resource_demands(path_name): return _read_csv_resource_file(path_name + '/resource_demands.csv')
def get_resource_provisions(path_name): return _read_csv_resource_file(path_name + '/resource_provisions.csv')

def write_csv_file(file_name, data):
	with open(file_name, 'w+', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		for row in data:
			writer.writerow(row)

def remove_file(path_name): 
     if file_exists(path_name): os.remove(path_name)

def file_exists(path_name):
     return os.path.isfile(path_name)

def write_unsat(path_name):
	open(path_name + '/unsat', 'w+')
      
def write_sat(path_name):
	open(path_name + '/sat', 'w+')