apiVersion: run.googleapis.com/v1
kind: Job
metadata:
  name: my-frodock-job-1738942414_92069bc9
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
            - /data/frodock_mount/TestDataset/4DEF-Test2/4DEF_r_u_ASA.pdb
            - /data/frodock_mount/TestDataset/4DEF-Test2/4DEF_l_u_ASA.pdb
            - 1738942414_92069bc9
            - /data/frodock_mount/output_1738942414_92069bc9/
            - 4
            - /data/frodock_mount/workdir_1738942414_92069bc9/
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