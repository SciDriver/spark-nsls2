#!/usr/bin/env python

import sys
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import h5py
from scipy import interpolate

from pyspark.sql import SparkSession

def get_fnames(env):

    from databroker import get_table,db

    df  = db.get_table(db[27223],fill=False)
    fnames = df['merlin1'].as_matrix()
    
    return fnames

def load_files(fnames):

    import filestore
    import filestore.api
    from TimepixHDF5Handler import TimepixHDF5Handler
    
    filestore.api.register_handler('TPX_HDF5', TimepixHDF5Handler, overwrite=True)

    for i in range(0, len(fnames)):
        t = 1.*np.fliplr(np.squeeze(np.asarray(filestore.api.get_data(fnames[i]))).T)

    return len(fnames)

if __name__ == "__main__":
    """
        Usage: spark-db [partitions]
    """
    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    print ("spark initialization ...");
    t1 = datetime.now();
    spark = SparkSession.builder.appName("spark-db").getOrCreate()
    t2 = datetime.now();
    print ("processing  time: ", (t2 - t1));

    print("getting fnames ...");
    t1 = datetime.now();
    fnames = spark.sparkContext.parallelize(range(0,1), 1).map(get_fnames).collect()
    t2 = datetime.now();
    print ("processing time: ", (t2 - t1), "fnames: ", len(fnames[0]))

    print("loading files ...");
    t1 = datetime.now();
    rdd = spark.sparkContext.parallelize(np.split(fnames[0], partitions), partitions)
    num_frames = rdd.map(load_files).collect()
    t2 = datetime.now();
    print ("processing time: ", (t2 - t1))
    for i in range(0, partitions):
        print(i, ", num_frames: ", num_frames[i])
        
    spark.stop()

    
