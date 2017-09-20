
The db2sharp data-intensive application that demonstrates the acceleration of
the databroker interface for accessing and preprocessing large ptychographic
datasets with the spark parallel platform. 

Running spark with jupyter
--------------------------

export PYSPARK_DRIVER_PYTHON='jupyter'
export PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port=7777'

pyspark --master local[35]

dbsharp.27223.ipynb









