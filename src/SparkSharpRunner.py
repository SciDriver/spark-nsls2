import os
import time
from datetime import timedelta, datetime, tzinfo

from pyspark import SparkContext
from pyspark.sql import SparkSession

def run_sharp(kvs):
    
    def inner_mpi(kvs):
          
        import time
        from datetime import timedelta, datetime, tzinfo
        import sharp
        import sharpnsls2

        # define the MPI enviromental variables
        
        hostname = os.uname()[1]
        hydra_proxy_port = os.getenv("HYDRA_PROXY_PORT")
        pmi_port = hostname + ":" + hydra_proxy_port
    
        os.environ["PMI_PORT"] = pmi_port
        os.environ["PMI_ID"]   = str(kvs['pid'])
        
        # Initialization
            
        sharpNSLS2 = sharpnsls2.PySharpNSLS2()
        sharpNSLS2.setGNode()
        sharpNSLS2.init(kvs['args'])     
    
        # Reconstruction
    
        niters = 101
        for i in range(niters):
            sharpNSLS2.step()        
        sharpNSLS2.writeImage()
        
    from multiprocessing import Process

    t1 = datetime.now(); 
    p = Process(target=inner_mpi, args = (kvs, ))
    p.start()
    p.join()
    t2 = datetime.now()
    
    return (t2 -t1)

class SparkSharpRunner:

    def __init__(self):

    def run_with_spark(self, args, partitions):

        spark = SparkSession.builder.appName("sharp.mpi.spark").getOrCreate()

        pmiserv_cmd  = '/GPFS/CENTRAL/XF03ID1/SHARP/opt/gpu-001/spark-mpi/bin/pmiserv '
        pmiserv_cmd += '-n ' + str(partitions)
        pmiserv_cmd += ' hello &'

        if os.system(pmiserv_cmd) != 0:
            print ("pmiserv: ERROR")
            return
        time.sleep(2)
    
        env = []
        for i in range(0, partitions):
            kvs = {'pid' : i, 'args' : args}
            env.append(kvs)
        
        rdd = spark.sparkContext.parallelize(env, partitions)
        tsharp = rdd.map(run_sharp).collect()

        if os.system("pkill -9 \"hydra_pmi_proxy\" &") != 0:
            print ("pkill: ERROR")
            return
        time.sleep(2)
    
        return tsharp

