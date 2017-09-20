# SPARK-NSLS2

The application of the Spark-MPI integrated platform for accelerating the NSLS-II data-intensive and compute-intensive
beamline tasks and building near-real-time processing pipelines. The rationale as well as general
description of this approach are provided in the NYSDS'17 presentation: "[Building Near-Real-Time Processing Pipelines with the Spark-MPI platform](https://github.com/SciDriver/spark-nsls2/blob/master/doc/Malitsky-Chaudhary-NYSDS17.pdf)", NYSDS, New York, August 7-9, 2017. The Spark-MPI approach is funded by
the DOE ASCR SBIR grant.

## Conceptual Demo

The Spark-MPI approach is illustrated within the following examples addressing
three major aspects of beamline processing applications :

* [db2sharp](https://github.com/SciDriver/spark-nsls2/blob/master/examples/db2sharp/db2sharp.27223.ipynb):
data-intensive application that demonstrates the acceleration
of the databroker interface for accessing and preprocessing large ptychographic
datasets with the Spark parallel platform

* [sharp-mpi](https://github.com/SciDriver/spark-nsls2/blob/master/examples/sharp-mpi/sharp.mpi.17554.ipynb): MPI/GPU ptychographic reconstruction application resolving both the GPU memory and performance
requirements of ptychographic experiments for processing large scans

* [kafka](https://github.com/SciDriver/spark-nsls2/tree/master/examples/kafka ):
composite end-to-end application that demonstrates the integration
of the databroker interface, kafka, and spark-mpi platforms for building near-real-time
beamline processing pipelines

## Prerequisites

* [databroker](https://github.com/NSLS-II/databroker): unified interface for various data sources at NSLS-II

* [spark-mpi](https://github.com/SciDriver/spark-mpi): data-intensive and compute-intensive platform

* [sharp-nsls2](https://github.com/camera-sharp/sharp-nsls2): GPU/MPI ptychographic application

