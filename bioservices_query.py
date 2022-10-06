"""
Developer: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu
Model Source: Elowitz and Leibler (2000) repressilator model
Model Publication DOI: 10.1038/35002125
Model BioModel ID: BIOMD0000000012
Model BioModel URL: https://www.ebi.ac.uk/biomodels/BIOMD0000000012

Description: Query KEGG database for example identifier using the bioservices package.
            Tet repressor protein KEGG Orthology term: http://identifiers.org/kegg.orthology/K18476

(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
from bioservices import *
import pandas as pd

# %% Store annotation information
# Select database
database = KEGG()

# Retrieve a KEGG entry
tetR_query = database.get("K18476")

# Build a dictionary to parse query
tetR_dict = database.parse(tetR_query)

# Show information about the query
print(tetR_dict['NAME'])
print(tetR_dict['BRITE'])

# Store collected metadata or experimental measurements
BIOMD0000000012_metadata = pd.DataFrame([[tetR_dict['NAME']],[tetR_dict['BRITE']]],
                                        ['BIOCHEMICAL SPECIES NAME','BRITE'])
BIOMD0000000012_metadata.to_excel('BIOMD0000000012_metadata.xlsx')