"""
Developer: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu
Model Source: Elowitz and Leibler (2000) repressilator model
Model Publication DOI: 10.1038/35002125
Model BioModel ID: BIOMD0000000012
Model BioModel URL: https://www.ebi.ac.uk/biomodels/BIOMD0000000012

Description: Program to generate and run a test suite on BIOMD0000000012.

(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import tellurium as te
import unittest
from SBMLLint.tools.sbmllint import lint
import numpy as np


# %% Build model-specific unit testing suite using unittest

# Implement class of helper functions for unit test suite
class BIOMD0000000012TestSuiteHelper:
    """
    Test suite helper functions for BIOMD0000000012.
    """

    def __init__(self, model):
        self.model = model

    def has_mass_balance_errors(self):
        """
        Use sbmllint to check if model has static mass-balance errors.
        Returns 'True' if there are mass-balance errors, 'False' if there are not.

        :return: bool
        """
        return lint(self.model.getCurrentAntimony(), mass_balance_check="games")

    # Check for complex eigen values
    def has_complex_eigen_vals(self):
        """
        Function to check if model (RoadRunner object instance) has complex eigenvalues.
        Returns 'True' if there is at least one complex eigenvalue, 'False' if there are only
        real-valued eigenvalues.

        :return: bool
        """
        eigen_vals = self.model.getFullEigenValues()
        return any(np.iscomplex(eigen_vals))

    # Add more helper functions to class as needed


# Implement unit test suite
class BIOMD0000000012TestSuite(unittest.TestCase):
    """
    Test suite for BIOMD0000000012.

    To set up the test suite, the user must supply an RoadRunner Object instance called MODEL.
    The model will also be simulated using Tellurium and libRoadRunner.
    """

    def setUp(self):
        self.model = MODEL
        self.data = self.model.simulate(0, 500, 50)

    def test_BIOMD0000000012_mass_balance(self):
        """
        Check if model system has mass balance errors.

        assertFalse() is a function of the unittest library which compares the value passed to the
        function to the boolean value 'False'. If there are mass-balance errors, the test value will
        return 'False' and the test will be failed. If there are no mass-balance errors, the test
        will be passed.
        """
        self.assertFalse(BIOMD0000000012TestSuiteHelper(model=self.model).has_mass_balance_errors())

    def test_BIOMD0000000012_eigen_vals(self):
        """
        Check if model system has complex eigenvalues after timecourse simulation.

        assertTrue() is a function of the unittest library which compares the value passed to the
        function to the boolean value 'True'. If there are complex eigenvalues, the test value will
        return 'True' and the test will be passed. If there are no complex eigenvalues, the test
        will be failed.
        """
        self.assertTrue(BIOMD0000000012TestSuiteHelper(model=self.model).has_complex_eigen_vals())


if __name__ == "__main__":
    # Load model from BioModels Database and store Antimony string
    BIOMD0000000012 = te.loadSBMLModel(
        "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml")

    # Declare the input MODEL for the test suite, a RoadRunner Object instance
    MODEL = BIOMD0000000012

    # Demonstrate that the error-free model has expected oscillatory dynamics
    MODEL.resetAll()
    MODEL.simulate(0, 100, 50)
    MODEL.plot()

    # Run unit test suite on the error-free model
    test_suite = unittest.TestLoader().loadTestsFromTestCase(BIOMD0000000012TestSuite)
    _ = unittest.TextTestRunner().run(test_suite)

    # Set the Hill coefficient parameter 'n' to 0 to remove oscillatory dynamics
    MODEL.resetAll()
    MODEL.n = 0

    # Demonstrate that the model containing an error has lost oscillatory dynamics
    MODEL.simulate(0, 10, 10)
    MODEL.plot()

    # Demonstrate that this error results in the failure of the test for complex eigenvalues
    # Run unit test suite on model with error:
    suite = unittest.TestLoader().loadTestsFromTestCase(BIOMD0000000012TestSuite)
    _ = unittest.TextTestRunner().run(suite)
