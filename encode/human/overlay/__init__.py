import pandas as pd
from mrbob.rendering import parse_variables
from encode.human.csvreader import parse


def pre_render(self):
    self.variables = parse_variables(self.variables)
    self.variables['dimensions'] = self.variables['dimensions'].split()
