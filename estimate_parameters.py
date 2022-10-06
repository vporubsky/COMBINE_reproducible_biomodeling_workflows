"""
Developer: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu
Model Source: Elowitz and Leibler (2000) repressilator model
Model Publication DOI: 10.1038/35002125
Model BioModel ID: BIOMD0000000012
Model BioModel URL: https://www.ebi.ac.uk/biomodels/BIOMD0000000012

Description: Program to estimate parameters for BIOMD0000000012.

(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import h5py
import tellurium as te
from BIOMD0000000012_study_utils import ParameterEstimation
import matplotlib.pyplot as plt

# %% Set up parameter estimation routine
import random
random.seed(155)

# Load synthetic dataset
DATA_H5F = h5py.File('BIOMD0000000012_synthetic_data.h5', 'r')
DATA = DATA_H5F['BIOMD0000000012_synthetic_dataset'][:]
DATA_H5F.close()

# Load model and specify parameters and parameter ranges for optimization
BIOMODELS_FILE_URL = 'https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml'
BIOMD0000000012 = te.loadSBMLModel(BIOMODELS_FILE_URL)

# Generate parameter dictionary:
# Dictionary uses the parameter name as a key
# and the minimum search value, initial search value, and maximum search value
# are provided as a tuple value for each key
BIOMD0000000012_PARAMETERS = {
    "n": (0.0001, 1, 5),
    "tau_mRNA": (0.0001, 1, 5),
    "ps_a": (0.0001, 1, 5),
    "ps_0": (0.0001, 1, 5)
}

# Choose species for fitting with synthetic data
SPECIES_SELECTIONS = ['PX', 'PY', 'PZ']

# Initialize ParameterEstimation object
BIOMD0000000012_pe = ParameterEstimation(model=BIOMD0000000012,
                                         data=DATA,
                                         params=BIOMD0000000012_PARAMETERS,
                                         species_selections=SPECIES_SELECTIONS)

# Minimize the objective using parameter ranges and lmfit
BIOMD0000000012_optimized_params = BIOMD0000000012_pe.optimize_parameters()
print(BIOMD0000000012_optimized_params.params)

#%%  Test solution to asses fit
# Reset concentrations to initial value and reset selections
BIOMD0000000012.reset()
BIOMD0000000012.resetSelectionLists()

# Simulate model with optimized parameters
BIOMD0000000012_SIMULATION = BIOMD0000000012.simulate(0, 500, 50)

# Plot simulated data and experimental data
plt.plot(DATA[:, 0], DATA[:, 1:4], '.')
plt.plot(BIOMD0000000012_SIMULATION[:, 0], BIOMD0000000012_SIMULATION[:, 1:4])
plt.show()

# %% Execute Monte Carlo
# Monte carlo
BIOMD0000000012_MC_DATA = BIOMD0000000012_pe.run_monte_carlo(num_itr=5,
                                                             optimized_params=BIOMD0000000012_optimized_params)

# Save new Monte Carlo results as hdf5:
BIOMD0000000012_MC_DATA.to_hdf('BIOMD0000000012_monte_carlo_data_.h5',
                               key='BIOMD0000000012_estimated_parameter_sets',
                               mode='w')

