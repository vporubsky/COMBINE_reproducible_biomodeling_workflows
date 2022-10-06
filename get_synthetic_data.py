"""
Developer: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu
Model Source: Elowitz and Leibler (2000) repressilator model
Model Publication DOI: 10.1038/35002125
Model BioModel ID: BIOMD0000000012
Model BioModel URL: https://www.ebi.ac.uk/biomodels/BIOMD0000000012

Description: Program to generate synthetic data for BIOMD0000000012.

(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import tellurium as te
import matplotlib.pyplot as plt
import h5py
from BIOMD0000000012_study_utils import get_data

if __name__ == "__main__":
    # Load model from BioModels Database
    BIOMODELS_FILE_URL = \
        'https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml'
    BIOMD0000000012 = te.loadSBMLModel(BIOMODELS_FILE_URL)

    # Declare species for which to generate experimental data
    SPECIES = ['PX', 'PY', 'PZ']

    # Get a synthetic dataset
    DATA = get_data(BIOMD0000000012, noise_level=0.2, time_start=0, time_end=500, num_pts=100, species=SPECIES)

    # Visualize noisy synthetic data
    plt.plot(DATA[:, 0], DATA[:, 1:], '.')
    plt.legend(SPECIES)
    plt.show()

    # Save HDF5 dataset
    h5f = h5py.File('BIOMD0000000012_synthetic_data.h5', 'w')
    h5f.create_dataset('BIOMD0000000012_synthetic_dataset', data=DATA)
    h5f.close()
