"""
Developer: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu
Model Source: Elowitz and Leibler (2000) repressilator model
Model Publication DOI: 10.1038/35002125
Model BioModel ID: BIOMD0000000012
Model BioModel URL: https://www.ebi.ac.uk/biomodels/BIOMD0000000012

Description: Program to simulate BIOMD0000000012 using Tellurium.

(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import tellurium as te
import phrasedml
import matplotlib.pyplot as plt
import os
import h5py

# Set base directory for imports and exports
BASE_DIR = os.getcwd()

# Load model from BioModels Database
BIOMD0000000012 = te.loadSBMLModel(
    "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml")

# Export SBML model file to current working directory
BIOMD0000000012.exportToSBML('BIOMD0000000012.xml')


# %% Write and export SED-ML using phraSED-ML

# Write phraSED-ML string specifying the simulation study
BIOMD0000000012_phrasedml = '''
  // Set model
  BIOMD0000000012 = model "BIOMD0000000012.xml" 

  // Deterministic simulation
  det_sim = simulate uniform(0, 500, 1000) # deterministic simulation from time 0 to 500 with 1000 points
  BIOMD0000000012_det_sim = run det_sim on BIOMD0000000012 # execute the deterministic simulation
  plot "Repressilator PX dynamics (Model ID: BIOMD0000000012)" time vs PX # plot time vs protein 'PX'
'''

# Generate SED-ML string from the phraSED-ML string
BIOMD0000000012.resetAll()
BIOMD0000000012_sbml = BIOMD0000000012.getSBML()
phrasedml.setReferencedSBML("BIOMD0000000012.xml", BIOMD0000000012_sbml)
BIOMD0000000012_sedml = phrasedml.convertString(BIOMD0000000012_phrasedml)

# Save the SED-ML simulation experiment to your current working directory
te.saveToFile(os.path.join(BASE_DIR, 'BIOMD0000000012_sedml.xml'), BIOMD0000000012_sedml)

# Load and run SED-ML script
te.executeSEDML(os.path.join(BASE_DIR, 'BIOMD0000000012_sedml.xml'))


#%% Generate COMBINE archive
# get Antimony string of BIOMD0000000012
BIOMD0000000012_antimony = te.readFromFile(os.path.join(BASE_DIR, 'BIOMD0000000012_antimony.txt'))

# create an inline OMEX string
BIOMD0000000012_inline_omex = '\n'.join([BIOMD0000000012_antimony, BIOMD0000000012_phrasedml])

# export to a COMBINE archive
BIOMD0000000012_combine_archive = os.path.join(BASE_DIR, 'BIOMD0000000012.omex')
te.exportInlineOmex(BIOMD0000000012_inline_omex, BIOMD0000000012_combine_archive)


#%% Simulate with Tellurium and libroadrunner and export model to SBML

# Run simulation from time 0 to 500, collecting 1000 time points
BIOMD0000000012_simulation = BIOMD0000000012.simulate(0, 500, 1000)

# Plot simulation results for visualization
BIOMD0000000012.plot(figsize=(10, 6),
                     xtitle='Time',
                     ytitle='Concentration')
plt.show()

#%% Store simulation results in HDF5

# write HDF5 file for simulation results
H5F = h5py.File('BIOMD0000000012_simulation_results.h5', 'w')
DATA = H5F.create_dataset('BIOMD0000000012_tellurium_simulation', data=BIOMD0000000012_simulation)

# Add metadata to the saved dataset
DATA.attrs['Version information'] = te.getVersionInfo()
DATA.attrs['BioModels Database ID'] = 'BIOMD0000000012'
DATA.attrs['Model system'] = 'repressilator'
H5F.close()

# Load and plot HDF5 dataset
DATA_H5F = h5py.File('BIOMD0000000012_simulation_results.h5', 'r')
DATA = DATA_H5F['BIOMD0000000012_tellurium_simulation'][:]

# Visualize simulation results
plt.plot(DATA[:,0], DATA[:,1:])

# View dataset attributes
for key in list(DATA_H5F['BIOMD0000000012_tellurium_simulation'].attrs.keys()):
    print(f"{key}: {DATA_H5F['BIOMD0000000012_tellurium_simulation'].attrs[key]}")

DATA_H5F.close()
