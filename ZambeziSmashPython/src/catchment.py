# Catchement class

import numpy as np

class Catchment:

   def __init__(self, name, model):
        # Explanation placeholder
        self.name = name
        self.model = model

        data_directory = "../data/"
        self.inflow = np.loadtxt(f"{data_directory}Inflow{name}.txt")