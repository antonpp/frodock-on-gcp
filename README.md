# frodock-on-gcp
Protein simulation with FRODOCK (Fast Rotational DOCKing) on GCP

```sh
gcloud run jobs create frodock-job --image antonpopovine/frodock-mpi --cpu 8 --memory 8G --args python3,/data/frodock_mount/scripts/run_frodock.py,/data/frodock_mount/TestDataset/1WEJ-Test2/1WEJ_r_u_ASA.pdb,/data/frodock_mount/TestDataset/1WEJ-Test2/1WEJ_l_u_ASA.pdb,test00,/data/frodock_mount/workdir/,4,/data/frodock_mount/workdir/
```

```sh
gcloud run jobs update frodock-job --add-volume name=gcs-mount,type=cloud-storage,bucket=gke-dja-demo_static_assets --add-volume-mount volume=gcs-mount,mount-path=/data
```