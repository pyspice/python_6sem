from collections import Generator
import numpy as np
import pandas as pd

class Agent(Generator):
    
    def __init__(self, kb, name):
        self.replicas = pd.read_csv(kb, encoding='utf-8')
        self.name = name
        self.n = 0

    def send(self, msg):
        return '\t{}: {}\n'.format(self.name, np.random.choice(self.replicas['text']))

    def throw(self, typ=None, val=None, tb=None):
        # Оставляем как есть
        super().throw(typ, val, tb)

    def __str__(self):
        return 'Agent({})'.format(self.name)

    def __repr__(self):
        return str(self)