import xnat

session = xnat.connect('https://xnat.health-ri.nl')
project = session.projects['stwstrategyhn1']

for subject in project.subjects:
    # Download all scans for the subject
    for experiment in subject.experiments:
        for scan in experiment.scans:
            print(f'Downloading {scan.uid} for subject {subject.label} in experiment {experiment.label}')
            # Create directory structure if it doesn't exist
            import os
            os.makedirs(f'./data/{subject.label}/{experiment.label}', exist_ok=True)
            # Download the scan to the specified directory
            scan.download(f'./data/{subject.label}/{experiment.label}/{scan.uid}')