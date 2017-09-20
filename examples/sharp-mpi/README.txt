This demo demonstrates the MPI/GPU ptychographic reconstruction application
resolving both the GPU memory and performance requirements of ptychographic
experiments for processing large scans.

1. Running spark with jupyter

export PYSPARK_DRIVER_PYTHON='jupyter'
export PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port=7777'

pyspark --master local[35]

sharp.mpi.17554.ipynb

2. Checking results

./show.17554.py





