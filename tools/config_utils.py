from z3 import *
import random

predefined_config = [
        (Bool('body-comfort-system'), True),
        (Bool('hmi'), True),
        (Bool('led'), False),
        (Bool('led-alarm-system'), False),
        (Bool('led-finger-protection'), False),
        (Bool('led-central-locking'), False),
        (Bool('led-power-window'), False),
        (Bool('led-exterior-mirror'), False),
        (Bool('led-em-heatable'), False),
        (Bool('door-system'), True),
        (Bool('exterior-mirror'), True),
        (Bool('em-electric'), True),
        (Bool('em-heatable'), False),
        (Bool('power-window'), True),
        (Bool('pw-finger-protection'), True),
        (Bool('pw-control'), True),
        (Bool('pw-manual'), True),
        (Bool('pw-automatic'), False),
        (Bool('security'), True),
        (Bool('rc-key'), False),
        (Bool('rck-pw-automatic'), False),
        (Bool('rck-exterior-mirror'), False),
        (Bool('rck-alarm-system'), False),
        (Bool('rck-safety-function'), False),
        (Bool('central-locking'), False),
        (Bool('central-locking-automatic'), False),
        (Bool('alarm-system'), True),
        (Bool('alarm-system-interior'), True)]

def encode_config(config): # config = [](z3_variable, selected)
    return ''.join([str(int(bool(selected))) for _, selected in config])

class ValidConfigGen:
    def __init__(self, cnf, features) -> None:
        self.s = Solver()
        self.seed = random.randint(0,sys.maxsize)
        set_option('smt.phase_selection', 5) # random
        set_option('sat.phase', 'random')
        set_option('smt.random_seed', self.seed)
        self.s.add(cnf)
        self.features = features
        self.sequence: str = ''
    
    def next(self):
        if self.s.check() == sat:
            m = self.s.model()
            self.s.add(Or([z3_feature != m.evaluate(z3_feature, model_completion=True) for _, z3_feature in self.features]))
            config = [(z3_feature, m[z3_feature]) for _, z3_feature in self.features]
            self.sequence += encode_config(config)
            return config
        else:
            print("No more valid configs possible.")
            return None
    
    def get_timings(self): return self.timings