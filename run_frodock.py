#!/usr/bin/env python

import subprocess
import sys
import os

# configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_frodock(receptor_file, ligand_file, dat_files_name, dat_dir, np, workdir):
    """
    Runs the FRODOCK program with the given parameters.

    Args:
        receptor_file: Path to the receptor PDB file.
        ligand_file: Path to the ligand PDB file.
        dat_files_name: Base name for the output .dat files.
        dat_dir: Directory to save the output .dat files.
        np: Number of processors to use (for MPI).
        workdir: Directory to prepend to output file paths.
    """

    pre = "./bin/"
    mympi = "mpirun"
    comp = "_gcc"

    receptor = os.path.splitext(receptor_file)[0]
    ligand = os.path.splitext(ligand_file)[0]

    receptor_base = os.path.basename(receptor)
    ligand_base = os.path.basename(ligand)

    print(f"Receptor base: {receptor_base}")
    print(f"Ligand base: {ligand_base}")

    if np >= 2:
        mpi = "_mpi"
        print(f"Using mpi version with {np} processors ({mympi} command)")
    else:
        mpi = ""
        print("Using single processor version")

    suff = mpi + comp
    suff2 = comp

    if mpi == "_mpi":
        run = [mympi, "-np", str(np)]
        print("RUNNING MPI TESTS")
    else:
        run = []
        print("RUNNING NON-MPI TESTS")

    def execute(cmd):
        """Executes a command with subprocess and prints output, handling non-zero exit codes."""
        print(" ".join(cmd))
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"WARNING: Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            # You can add more specific error handling here if needed, e.g.,
            # if e.returncode == 1:
            #     print("Error code 1: ...")

    # Create output directory if it doesn't exist
    os.makedirs(dat_dir, exist_ok=True)

    dock_dat_file = os.path.join(dat_dir, f"{dat_files_name}_dock.dat")
    clust_dock_dat_file = os.path.join(dat_dir, f"{dat_files_name}_clust_dock.dat")

    # STAGE-1 Creation of receptor vdw potential map
    logger.info("STAGE-1 Creating receptor vdw potential map")
    execute(run + [pre + 'frodockgrid' + suff, receptor_file, "-o", os.path.join(workdir, receptor_base + '_W.mrc')])

    # STAGE-2 Creation of the receptor electrostatic potential map
    logger.info("STAGE-2 Creating receptor electrostatic potential map")
    execute(run + [pre + 'frodockgrid' + suff, receptor_file, "-o", os.path.join(workdir, receptor_base + '_E.mrc'), "-m", "1", "-t", "A"])

    # STAGE-3 Creation of the receptor desolvation potential map
    logger.info("STAGE-3 Creating receptor desolvation potential map")
    execute(run + [pre + 'frodockgrid' + suff, receptor_file, "-o", os.path.join(workdir, receptor_base + '_DS.mrc'), "-m", "3"])

    # STAGE-4 Creation of the ligand desolvation potential map
    logger.info("STAGE-4 Creating ligand desolvation potential map")
    execute(run + [pre + 'frodockgrid' + suff, ligand_file, "-o", os.path.join(workdir, ligand_base + '_DS.mrc'), "-m", "3"])

    # STAGE-5 Performing the docking 
    logger.info(f"STAGE-5 Performing the docking")
    execute(run + [pre + 'frodock' + suff, receptor + '_ASA.pdb', ligand + '_ASA.pdb',
                    "-w", os.path.join(workdir, receptor_base + '_W.mrc'), "-e", os.path.join(workdir, receptor_base + '_E.mrc'), "--th", "10",
                    "-d", os.path.join(workdir, receptor_base + '_DS.mrc')+','+os.path.join(workdir, ligand_base + '_DS.mrc'), "-t", "A", "-o", dock_dat_file, 
                    "-s", pre + 'soap.bin'])

    # STAGE-6 Clustering and visualization of predictions
    logger.info("STAGE-6 Clustering and visualization of predictions")
    execute([pre + 'frodockcluster' + suff2, dock_dat_file, ligand_file, "--nc", "100", "-o", clust_dock_dat_file])

    # STAGE-7 Visualize the first 20 solutions
    logger.info("STAGE-7 Visualize the first 20 solutions")
    execute([pre + 'frodockview' + suff2, clust_dock_dat_file, "-r", "1-20"])

    # STAGE-8 Coordinate generation of the 10 best predicted solutions
    logger.info("STAGE-8 Coordinate generation of the 10 best predicted solutions")
    execute([pre + 'frodockview' + suff2, clust_dock_dat_file, "-r", "1-10", "-p", ligand_file])

    print("\nRUN FINISHED\n")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python frodock.py <receptor_file> <ligand_file> <dat_files_name> <dat_dir> <np> <workdir>")
        sys.exit(1)

    receptor_file = sys.argv[1]
    ligand_file = sys.argv[2]
    dat_files_name = sys.argv[3]
    dat_dir = sys.argv[4]
    np = int(sys.argv[5])
    workdir = sys.argv[6]

    run_frodock(receptor_file, ligand_file, dat_files_name, dat_dir, np, workdir)