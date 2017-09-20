The composite end-to-end application that demonstrates the integration of
the databroker interface, kafka and spark-mpi platforms for building
near-real-time beamline processing pipelines


1. Start the Zookeeper server (port: 2181) and 
the Kafka server (port: 9092), check topics

zookeeper-server-start.sh zookeeper.properties &
kafka-server-start.sh server.properties &
kafka-topics.sh --list --zookeeper localhost:2181

2. Run the Spark-Kafka consumer for processing datbaroker's frames
with the Sharp-NSLS2 multi-GPU ptychographic application

export PYSPARK_DRIVER_PYTHON='jupyter'
export PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port=7777'
export HYDRA_PROXY_PORT=55555

pyspark --master local[35]

consumer.sharp.mpi.17554.ipynb

3. Run (in the different terminal) the Kafka producer
of datbaroker's frames and scan points

python producer.db2sharp.17554.py

4. Stop the Kafka and Zookeeper servers

kafka-server-stop.sh
zookeeper-server-stop.sh

