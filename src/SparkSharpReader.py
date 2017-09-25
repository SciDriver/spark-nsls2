from datetime import datetime

import numpy as np
import h5py

from databroker import get_table,db
from pyspark.sql import SparkSession

from SharpReader import SharpReader

def load_files(kvs):
    
    from SharpReader import SharpReader
    sharpReader = SharpReader()
    
    # x_c, y_c, xn, yn, threshold
    sharpReader.init(kvs['x_c'], kvs['y_c'],
                     kvs['nx'], kvs['ny'],
                     kvs['threshold'])
    
    frames = sharpReader.load_files(kvs['sid'], kvs['fnames'], kvs['ic'])
    
    frmfile = './npys/frames.' + str(kvs['sid']) + '.' + str(kvs['pid']) + '.npy'
    np.save(frmfile, frames)
    
    return frmfile

class SparkSharpReader(SharpReader):
    
    def __init__(self):
        SharpReader.__init__(self)

    def load_files_with_spark(self, sid, fnames, ic, partitions):

        spark = SparkSession.builder.appName("db2sharp.spark").getOrCreate()
      
        pfnames = np.split(fnames, partitions)
        pics    = np.split(ic, partitions)

        env = []
        for i in range(0, partitions):
            kvs = {
                'x_c' : self.x_c, 'y_c' : self.y_c,
                'nx' : self.nx, 'ny' : self.ny, 'threshold' : self.threshold,
                'pid' : i, 'sid' : sid, 'fnames' : pfnames[i], 'ic' : pics[i]
            }
            env.append(kvs)
    
        rdd = spark.sparkContext.parallelize(env, partitions)
        frmfiles = rdd.map(load_files).collect()

        # for i in range(0, partitions):
        #    print(i, ", frmfile: ", frmfiles[i])

        aframes = []
        for frmfile in frmfiles:
            pframes = np.load(frmfile)
            aframes.append(pframes)
         
        frames = np.concatenate(aframes)

        return frames

