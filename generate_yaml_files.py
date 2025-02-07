import yaml
import argparse
import time
import hashlib
from pathlib import Path
import os



def generate_frodock_yaml(receptor_file, ligand_file, data_files_name, data_files_dir, npi_setting, work_dir):
    """Generates a YAML Kubernetes spec file for a Frodock job."""

    base_template = """
apiVersion: run.googleapis.com/v1
kind: Job
metadata:
  name: my-frodock-job
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/client-name: cloud-console
        run.googleapis.com/execution-environment: gen2
      labels:
        cloud.googleapis.com/location: europe-west1
    spec:
      taskCount: 1
      template:
        spec:
          containers:
          - args:
            - python3
            - /data/frodock_mount/scripts/run_frodock.py
            - {receptor_file}
            - {ligand_file}
            - {data_files_name}
            - {data_files_dir}
            - {npi_setting}
            - {work_dir}
            image: antonpopovine/frodock-mpi
            name: my-frodock-job-1
            resources:
              limits:
                cpu: 8000m
                memory: 8Gi
            volumeMounts:
            - mountPath: /data
              name: gcs-mount
          maxRetries: 3
          timeoutSeconds: '1200'
          volumes:
          - csi:
              driver: gcsfuse.run.googleapis.com
              volumeAttributes:
                bucketName: gke-dja-demo_static_assets
            name: gcs-mount
    """

    yaml_data = yaml.safe_load(base_template.format(
        receptor_file=receptor_file,
        ligand_file=ligand_file,
        data_files_name=data_files_name,
        data_files_dir=data_files_dir,
        npi_setting=npi_setting,
        work_dir=work_dir
    ))

    yaml_string = yaml.dump(yaml_data, default_flow_style=False)
    return yaml_string


def write_yaml_to_file(yaml_string, receptor_file):
    """Writes the YAML string to a file with a timestamp and hash in the name,
       using the receptor file path as a base.
    """

    timestamp = str(int(time.time()))
    file_hash = hashlib.sha256(yaml_string.encode()).hexdigest()[:8]  # Short hash

    base_filename = os.path.basename(receptor_file)
    base_name_without_ext = os.path.splitext(base_filename)[0]

    filename = f"{base_name_without_ext}_{timestamp}_{file_hash}.yaml"
    filepath = Path(filename)

    try:
        with filepath.open("w") as f:
            f.write(yaml_string)
        print(f"YAML written to {filename}")
        return filepath
    except Exception as e:
        print(f"Error writing to file: {e}")
        return None


if __name__ == "__main__":

    # Sample input tuples (receptor, ligand)
    input_tuples = [
        ("/data/frodock_mount/TestDataset/1WEJ-Test2/1WEJ_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/1WEJ-Test2/1WEJ_l_u_ASA.pdb"),
        ("/data/frodock_mount/TestDataset/2XYZ-Test2/2XYZ_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/2XYZ-Test2/2XYZ_l_u_ASA.pdb"),
        ("/data/frodock_mount/TestDataset/3ABC-Test2/3ABC_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/3ABC-Test2/3ABC_l_u_ASA.pdb"),
        ("/data/frodock_mount/TestDataset/4DEF-Test2/4DEF_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/4DEF-Test2/4DEF_l_u_ASA.pdb"),
        ("/data/frodock_mount/TestDataset/5GHI-Test2/5GHI_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/5GHI-Test2/5GHI_l_u_ASA.pdb"),
        ("/data/frodock_mount/TestDataset/6JKL-Test2/6JKL_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/6JKL-Test2/6JKL_l_u_ASA.pdb"),
        ("/data/frodock_mount/TestDataset/7MNO-Test2/7MNO_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/7MNO-Test2/7MNO_l_u_ASA.pdb"),
        ("/data/frodock_mount/TestDataset/8PQR-Test2/8PQR_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/8PQR-Test2/8PQR_l_u_ASA.pdb"),
        ("/data/frodock_mount/TestDataset/9STU-Test2/9STU_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/9STU-Test2/9STU_l_u_ASA.pdb"),
        ("/data/frodock_mount/TestDataset/0VWX-Test2/0VWX_r_u_ASA.pdb", "/data/frodock_mount/TestDataset/0VWX-Test2/0VWX_l_u_ASA.pdb"),
    ]

    npi_setting = 4  # Set npi_setting to 4

    for receptor_file, ligand_file in input_tuples:
        timestamp = int(time.time())
        hash_str = hashlib.sha256(str(timestamp).encode()).hexdigest()[:8]  # Short hash

        data_files_name = f"{hash_str}"
        work_dir = f'/data/frodock_mount/workdir_{hash_str}/'
        data_files_dir = f'/data/frodock_mount/output_{hash_str}/'

        yaml_spec = generate_frodock_yaml(receptor_file, ligand_file, data_files_name, data_files_dir, npi_setting, work_dir)
        filepath = write_yaml_to_file(yaml_spec, receptor_file)
        if filepath:
            print(f"File saved to: {filepath}")
        else:
            print("Failed to save the file.")