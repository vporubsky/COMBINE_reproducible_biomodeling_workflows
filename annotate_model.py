"""
Developer: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu
Model Source: Elowitz and Leibler (2000) repressilator model
Model Publication DOI: 10.1038/35002125
Model BioModel ID: BIOMD0000000012
Model BioModel URL: https://www.ebi.ac.uk/biomodels/BIOMD0000000012
Description: Program to annotate BIOMD0000000012 using sbmlutils.
(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import tellurium as te
from sbmlutils.metadata.annotator import ModelAnnotator, annotate_sbml
from pathlib import Path
import os

# Read and print the annotation file, stored as an .xlsx table
BIOMD0000000012_ANNOTATIONS = ModelAnnotator.read_annotations_df('BIOMD0000000012_annotations.xlsx',
                                                                 file_format="xlsx")
print(BIOMD0000000012_ANNOTATIONS.to_markdown())

# Set base directory for annotation filepath
BASE_DIR = os.getcwd()

# Annotate existing BIOMD0000000012 SBML
BIOMD0000000012_doc = annotate_sbml(
    source=Path(os.path.join(BASE_DIR, 'BIOMD0000000012.xml')),
    annotations_path=Path(os.path.join(BASE_DIR, 'BIOMD0000000012_annotations.xlsx')),
    filepath=Path(os.path.join(BASE_DIR, 'BIOMD0000000012_annotated.xml'))
)

# Save annotated SBML string to file in working directory
BIOMD0000000012_ANNOTATED_SBML = BIOMD0000000012_doc.getSBMLDocument().toSBML()
te.saveToFile(os.path.join(BASE_DIR, 'BIOMD0000000012_annotated.xml'),
              BIOMD0000000012_ANNOTATED_SBML)
