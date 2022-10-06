"""
Developer: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu
Model Source: Elowitz and Leibler (2000) repressilator model
Model Publication DOI: 10.1038/35002125
Model BioModel ID: BIOMD0000000012
Model BioModel URL: https://www.ebi.ac.uk/biomodels/BIOMD0000000012

Description: Program to import BIOMD0000000012 SBML file from BioModels Database
and visualize the biological system/ network using an SBGN file.

(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import tellurium as te
import matplotlib.pyplot as plt
from IPython.display import Image
import tempfile
from libsbgnpy import render, utils

# Load model from BioModels Database
BIOMD0000000012 = te.loadSBMLModel(
    "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml")

# Simulate model and visualize output
simulation_result = BIOMD0000000012.simulate(0, 500, 1000)
BIOMD0000000012.plot(figsize=(10, 6), xtitle='Time', ytitle='Concentration')
plt.show()

# %% Visualize model network with SBGN
# BIOMD0000000012.sbgn generated using CellDesigner export SBGN-ML.
BIOMD0000000012_sbgn = utils.read_from_file("BIOMD0000000012.sbgn")
BIOMD0000000012_png = tempfile.NamedTemporaryFile(suffix=".png")
render.render_sbgn(BIOMD0000000012_sbgn,
                   image_file=BIOMD0000000012_png.name,
                   file_format="png")
Image(BIOMD0000000012_png.name, width=500)
