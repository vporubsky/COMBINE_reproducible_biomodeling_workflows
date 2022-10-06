"""
Developer Name: Veronica Porubsky
Developer ORCID: 0000-0001-7216-3368
Developer GitHub Username: vporubsky
Developer Email: verosky@uw.edu

File Creation Date: 
File Final Edit Date:

Description: 
"""
import os
import json
import fire
import requests
biosimulations_runs_file = "biosimulations_runs.json"


def runProject(project_id, simulator='tellurium', omex_dir="./omex_files"):
    """
    This function runs the project on biosimulations.
    """
    omex_file = os.path.join(omex_dir, project_id + ".omex")

    simulation_run_data = {
        'name': project_id,
        'simulator': simulator,
        'version': 'latest',
    }

    multipart_form_data = {
        'file': ('archive.omex', open(omex_file, 'rb')),
        'simulationRun': (None, json.dumps(simulation_run_data)),

    }

    req = requests.post(
        "https://api.biosimulations.org/runs",
        files=multipart_form_data)
    req.raise_for_status()
    res = req.json()
    simulation_id = res["id"]
    if(os.path.exists(biosimulations_runs_file)):
        with open(biosimulations_runs_file) as f:
            runs = json.load(f)
    else:
        runs = {}
    runs[project_id] = simulation_id

    with open(biosimulations_runs_file, 'w') as f:
        json.dump(runs, f)

    print("Ran " + project_id + " on biosimulations with simulation id: " + simulation_id)
    print("View: https://run.biosimulations.org/runs/" + simulation_id)


if __name__ == "__main__":
    fire.Fire(runProject)