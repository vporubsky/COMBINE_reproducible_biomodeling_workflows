"""
Developer: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu
Model Source: Elowitz and Leibler (2000) repressilator model
Model Publication DOI: 10.1038/35002125
Model BioModel ID: BIOMD0000000012
Model BioModel URL: https://www.ebi.ac.uk/biomodels/BIOMD0000000012

Description: Supplemental utilities for MiMB reproducible modeling study.

(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import numpy as np
from lmfit import Minimizer, Parameters, Parameter
import random
import pandas as pd

# %% DATA GENERATION
def get_data(model, noise_level=0.5, time_start=0, time_end=10, num_pts=10, species=None):
    """
    Returns a noisy synthetic dataset for the specified model to mimic
    experimental results, as a numpy.ndarray.

    The first column of the returned array contains collection times
    for each data point.
    Subsequent columns contain concentrations of biochemical species
    in the model collected at each time specified in the first column.

    :param model: RoadRunner object instance
    :param noise_level: float: [0,1]
    :param time_start: float
    :param time_end: float
    :param num_pts: int:  number of points to sample
    :param species: list of str: species names matching model identifiers
    :return: numpy.ndarray: time in first column, followed by columns of species
        concentrations over timecourse
    """
    # Reset model to original state
    model.resetAll()

    # Run simulation, store sampling times and data (concentration measurements)
    if species is None:
        simulation_result = model.simulate(time_start, time_end, num_pts)
    else:
        simulation_result = model.simulate(time_start, time_end, num_pts, ['time'] + species)

    # Create matrix of Gaussian distributed noise
    noise = np.random.normal(0, 1, simulation_result.shape)
    for col_idx in range(np.shape(noise)[1]):
        if col_idx == 0:
            # Set first column to 0 (time samples will be unchanged in subsequent step)
            noise[:, col_idx] *= 0
        else:
            # Scale noise matrix using noise_level parameter and the max
            # value for each species in the simulated model
            noise[:, col_idx] *= max(simulation_result[:, col_idx]) * noise_level

    # Add noise to simulation result
    # Set negative values to zero for physiological relevance
    noised_data = np.where(simulation_result + noise < 0, 0, simulation_result + noise)
    return noised_data


# %% PARAMETER ESTIMATION
class ParameterEstimation:
    """
    Provides parameter estimation functionality for the MiMB reproducible modeling study
    of BIOMD0000000012 using lmfit package.
    """
    def __init__(self, model, data, params, species_selections):
        """
        User supplies a RoadRunner object instance of the model system being studied,
        and experimental data in a numpy.ndarray object with the first column containing
        the time points at which the data was sampled.

        User passes a dictionary containing the parameters to be optimized and the
        corresponding initial values and ranges for the optimization routine. The
        dictionary keys must match the parameter ids used by the RoadRunner object
        instance to simulate the model.

        The species for which data was collected in the columns of the provided dataset
        must be passed. The names of the species must match the ids used by the RoadRunner
        object instance to simulate the model.

        :param model: RoadRunner object instance:
                Model generated using tellurium.loada(antimony_str) or tellurium.loadSBMLModel(SBML_str)
        :param data: numpy.ndarray:
                First column must contain times at which each data point was sampled.
        :param params: dict: params={ "param_1": (lower_bound, init_value, upper_bound),...
                "param_n" : (lower_bound, init_value, upper_bound)}
        :param species_selections: list: contains list of species measured in the provided dataset
        """
        self.model = model
        self.data = data
        self.time_start = data[0, 0]
        self.time_end = data[-1, 0]
        self.num_pts = np.shape(data)[0]
        self.species_selections = species_selections
        self.param_ids = list(params.keys())
        self.param_ranges = list(params.values())
        self.num_params = len(self.param_ids)

    def get_parameters(self):
        """
        Creates lmfit Parameters object to use in minimization routine.

        :return: lmfit Parameters() object
        """
        parameters = Parameters()
        for idx, param_id in enumerate(self.param_ids):
            parameters[param_id] = Parameter(name=param_id,
                                             value=self.param_ranges[idx][1],
                                             min=self.param_ranges[idx][0],
                                             max=self.param_ranges[idx][2])
        return parameters

    def get_residuals(self, parameters):
        """
        Objective function for minimization routine which returns the difference between
        the model prediction and a ground truth dataset.

        :param parameters: lmfit Parameters object
        :return: numpy.ndarray
        """
        self.model.resetAll()
        vals = parameters.valuesdict()
        for param in list(vals.keys()):
            self.model.setValue(param, vals[param])
        model_prediction = self.model.simulate(self.time_start,
                                               self.time_end,
                                               self.num_pts,
                                               self.species_selections)
        return np.abs(model_prediction - self.data[:, 1:])

    def get_optimized_simulation_data(self, optimized_params):
        """
        Returns simulation data for the specified model using optimized parameters.

        :param optimized_params: lmfit.minimizer.MinimizerResult
        :return: numpy.ndarray
        """
        self.model.reset()
        for param in self.param_ids:
            self.model.setValue(param, optimized_params.params.valuesdict()[param])
        return self.model.simulate(self.time_start,
                                   self.time_end,
                                   self.num_pts,
                                   self.species_selections)

    def get_optimized_residuals(self, optimized_params):
        """
        Returns residuals for the specified model using optimized parameters.

        :param optimized_params: lmfit.minimizer.MinimizerResult
        :return: numpy.ndarray
        """
        model_prediction = self.get_optimized_simulation_data(optimized_params)
        return np.abs(model_prediction - self.data[:, 1:])

    @staticmethod
    def __get_bootstrap_dataset(model_prediction, residuals, time):
        """
        Returns a bootstrapped dataset using optimized simulation data and randomly sampled residuals.

        :param model_prediction: RoadRunner NamedArray
        :param residuals: numpy.ndarray
        :param time: numpy.ndarray
        :return: numpy.ndarray
        """
        # Generate bootstrap dataset by randomly sampling from the residual distribution
        # and adding the residual to a parameter optimized simulation model_prediction
        bootstrap_data = np.zeros((np.shape(model_prediction)))
        for i in range(np.shape(bootstrap_data)[0]):
            for j in range(np.shape(bootstrap_data)[1]):
                bootstrap_data[i, j] = model_prediction[i, j] + random.choice(random.choice(residuals))

        # Set negative values to zero for physiological relevance
        synthetic_data = np.where(bootstrap_data < 0, 0, bootstrap_data)
        return np.insert(synthetic_data, 0, time, axis=1)

    def optimize_parameters(self):
        """
        Optimizes parameters using lmfit Minimizer.minimize routine.

        :return: lmfit.minimizer.MinimizerResult
        """
        fitter = Minimizer(userfcn=self.get_residuals, params=self.get_parameters())
        return fitter.minimize(method='differential_evolution')

    def run_monte_carlo(self, num_itr, optimized_params=None):
        """
        Performs bootstrapping of residuals to generate new synthetic data which approximates
        the noise in the original fitting dataset. Uses an optimized parameter set to initiate estimation.
        Executes the specified number of iterations to provide a distribution of parameter values.

        An added constraint checks that the system has complex eigenvalues because the system
        studied in the MiMB reproducible modeling study, the repressilator model BIOMD0000000012,
        is known to exhibit oscillatory dynamics.

        :param num_itr: int:
            Number of bootstrapping iterations to perform.
        :param optimized_params: lmfit.minimizer.MinimizerResult:
            Result of ParameterEstimation.optimize_parameters() method.
        :return: pandas.DataFrame
        """
        # Initialize Monte Carlo routine with model prediction, residuals, and a Monte Carlo array to store results
        if optimized_params is not None:
            pass
        else:
            optimized_params = self.optimize_parameters()
        model_prediction = self.get_optimized_simulation_data(optimized_params=optimized_params)
        residuals = self.get_optimized_residuals(optimized_params=optimized_params)
        mc_array = np.zeros((num_itr, len(self.param_ids)))

        # Perform bootstrapping optimization iterations
        for itr in range(num_itr):
            # Generate new bootstrapped dataset
            self.data = self.__get_bootstrap_dataset(model_prediction=model_prediction,
                                                     residuals=residuals,
                                                     time=self.data[:, 0])
            # Reset model parameters and concentrations
            self.model.resetAll()

            # Perform optimization
            optimization_successful = False
            while not optimization_successful:
                try:
                    optimized_params = self.optimize_parameters()
                    # Evaluate constraint: system has complex eigenvalues due to known
                    # oscillatory dynamics of BIOMD0000000012
                    if np.iscomplex(self.model.getFullEigenValues()).any():
                        optimization_successful = True
                except RuntimeError:
                    continue

            # Store optimized parameter values in array
            for param_idx, param in enumerate(self.param_ids):
                mc_array[itr, param_idx] = optimized_params.params.valuesdict()[param]

        # Return pandas.DataFrame containing sets of optimized parameter values
        return pd.DataFrame(mc_array, columns=self.param_ids)

# %% PARAMETER ESTIMATION FIGURES
import matplotlib.pyplot as plt
from math import pi

def set_radar_plot_properties(data):
    ''' Sets properties to plot radar plots.'''
    categories = list(data.keys())
    N = len(categories)

    # Axis angles
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise radar plot
    ax = plt.subplot(111, polar=True)

    # Draw one axis per parameter, and add parameter names
    plt.xticks(angles[:-1], categories)

    # Draw parameter value labels
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4], ["1", "2", "3", "4"], color="grey", size=7)
    plt.ylim(0, 5)

    return ax, angles