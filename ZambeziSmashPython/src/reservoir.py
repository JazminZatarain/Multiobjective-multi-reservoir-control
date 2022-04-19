# Reservoir class

import numpy as np

class Reservoir:
    """
    A class used to represent reservoirs of the problem

    Attributes
    ----------
    name : str
        Lowercase non-spaced name of the reservoir
    evap_rates : np.array
        (unit)
        Monthly evaporation rates of the reservoir throughout the run
    rating_curve : np.array (...x...)
        (unit) xUnit -> yUnit
        Vectors of water level versus corresponding discharge
    level_to_storage_rel : np.array (2x...)
        (unit) xUnit -> yUnit
        Vectors of water level versus corresponding water storage
    level_to_surface_rel : np.array (2x...)
        (unit) xUnit -> yUnit
        Vectors of water level versus corresponding surface area
    average_cross_section : float
        m2
        Average cross section of the reservoir. Used for approximation
        when relations are not given
    initial_storage : float
        m3
        Initial volume of water in the reservoir
    target_hydropower_production : np.array (12x1)
        TWh(?)
        Target hydropower production from the dam
    storage_vector : np.array (1xH)
        m3
        A vector that holds the volume of the water body in the reservoir
        throughout the simulation horizon
    level_vector : np.array (1xH)
        m
        A vector that holds the height of the water body in the reservoir
        throughout the simulation horizon
    release_vector : np.array (1xH)
        m3/s
        A vector that holds the release decisions from the reservoir
        throughout the simulation horizon

    Methods
    -------
    storage_to_level(h=float)
        Returns the level(height) based on volume
    level_to_storage(s=float)
        Returns the volume based on level(height)
    level_to_surface(h=float)
        Returns the surface area based on level
    integration()
        FILL IN LATER!!!!
    """

    def __init__(self, name, model):
        # Explanation placeholder
        self.name = name
        self.model = model

        data_directory = "../data/"
        self.evap_rates = np.loadtxt(f"{data_directory}evap_{name}.txt")
        self.rating_curve = np.loadtxt\
            (f"{data_directory}min_max_release_{name}.txt")
        self.level_to_storage_rel = np.loadtxt\
            (f"{data_directory}lsto_rel_{name}.txt")
        self.level_to_surface_rel = np.loadtxt\
            (f"{data_directory}lsur_rel_{name}.txt")
        self.average_cross_section = None # To be set in the model main file
        self.initial_storage = None # To be set in the model main file
        self.target_hydropower_production = None # To be set if obj exists
        self.storage_vector = np.empty(0)
        self.level_vector = np.empty(0)
        self.release_vector = np.empty(0)
        self.hydropower_plants = list()
        self.actual_hydropower_production = np.empty(0)
        self.hydropower_deficit = np.empty(0)

    def read_hydropower_target(self):
        self.target_hydropower_production = \
            np.loadtxt(f"..data/{self.name}prod.txt")
    
    def storage_to_level(self, s):
        # interpolation when lsto_rel exists
        if(self.level_to_storage_rel.size>0):
            h = self.interp_lin(self.level_to_storage_rel[1],
                self.level_to_storage_rel[0],s)
        # approximating with volume and cross section
        else:
            h = s/self.average_cross_section
        return h

    def level_to_storage(self, h):
        # interpolation when lsto_rel exists
        if(self.level_to_storage_rel.size>0):
            s = self.interp_lin(self.level_to_storage_rel[0],
                self.level_to_storage_rel[1],h)
        # approximating with volume and cross section
        else:
            s = h*self.average_cross_section
        return s

    def level_to_surface(self, h):
        # interpolation when lsur_rel exists
        if(self.level_to_surface_rel.size>0):
            a = self.interp_lin(self.level_to_surface_rel[0],
                self.level_to_surface_rel[1],h)
        # approximating with volume and cross section
        else:
            a = self.average_cross_section
        return a

    def integration(self, nu_of_days, policy_release_decision,
        net_secondly_inflow, current_month):
        """Converts the flows of the reservoir into storage. Time step
        fidelity can be adjusted within a for loop. The core idea is to
        arrive at m3 storage from m3/s flows.

        Parameters
        ----------

        Returns
        -------
        """
        # Record level and surface area based on received storage for time t:
        self.level_vector = np.append(self.level_vector,
            self.storage_to_level(self.storage_vector[-1]))
        average_surface_area = self.level_to_surface(self.level_vector[-1])
        
        # Calculate total m3 of water to add to the dam this month:
        total_seconds = 3600*24*nu_of_days
        total_addition_to_stock = total_seconds * net_secondly_inflow

        # Calculate total evaporation occured in the month
        total_evap = (self.evap_rates[current_month-1]/1000) * average_surface_area
        
        # Calculate min/max possible releases to compare with the policy decision
        # Kafue Gorge Lower reservoir needs a special treatment
        try:
            min_possible_release = self.interp_lin(self.rating_curve[0],
                self.rating_curve[1], self.level_vector[-1])
            max_possible_release = self.interp_lin(self.rating_curve[0],
                self.rating_curve[2], self.level_vector[-1])
        except IndexError:
            # Calculate monthly KGL storage average without release
            min_possible_release = 0
            average_storage_this_month = (self.level_vector[-1] + \
            (self.level_vector[-1] + total_addition_to_stock - total_evap)) / 2
            if average_storage_this_month <= self.rating_curve[0]:
                max_possible_release = 0
            elif (average_storage_this_month > self.rating_curve[0]) and \
                (average_storage_this_month <= self.rating_curve[1]):
                max_possible_release = average_storage_this_month - \
                    self.rating_curve[0] / total_seconds
            else:
                max_possible_release = self.rating_curve[2]

        actual_secondly_release = min(max_possible_release,
            max(min_possible_release, policy_release_decision))


        total_release = total_seconds * actual_secondly_release

        new_storage = self.storage_vector[-1] + total_addition_to_stock - \
            (total_release + total_evap)

        self.storage_vector = np.append(self.storage_vector, new_storage)
        self.release_vector = np.append(self.release_vector,
            actual_secondly_release)

    

    @staticmethod
    def interp_lin(X, Y, x):
        """Takes two vectors and a number. Based on the relative position
        of the number in the first vector, returns a number that has the
        equivalent relative position in the second vector.

        Parameters
        ----------
        X : np.array
            The array/vector that defines the axis for the input
        Y : np.array
            The array/vector that defines the axis for the output
        x : float
            The input for which an extrapolation is seeked

        Returns
        -------
        y : float
            Inter/Extrapolated output 
        """
        dim = X.size - 1

        # extreme cases (x<X(0) or x>X(end): extrapolation
        if(x <= X[0]):
            y = (Y[1] - Y[0]) / (X[1] - X[0]) * (x - X[0]) + Y[0] 
            return y
        
        elif(x >= X[dim]):
            y = Y[dim] + (Y[dim] - Y[dim-1]) / (X[dim] - X[dim-1]) * \
                (x - X[dim])
            return y
        
        # otherwise
        # [ x - X(A) ] / [ X(B) - x ] = [ y - Y(A) ] / [ Y(B) - y ]
        # y = [ Y(B)*x - X(A)*Y(B) + X(B)*Y(A) - x*Y(A) ] / [X(B) - X(A)]
        else:
            for index, item in enumerate(X):
                if x == item:
                    return Y[index]
                elif x < item:
                    a = (Y[index] - Y[index-1]) / (X[index] - X[index-1])
                    y = Y[index] - a*(X[index]-x)
                    return y
