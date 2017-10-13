#!/usr/bin/env python

from kafka import KafkaProducer

from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import h5py

import pickle

import databroker
from databroker import list_configs
from databroker import Broker
from hxntools.handlers import register

from SharpWriter import SharpWriter

sid = 26

# print("databroker version: ", databroker.__version__)
# print("configirations: ", list_configs())
# select the demo configuration
db = Broker.named('demo')
register(db)

# get the document header for the selected run
header = db[17554]

# Db2Sharp scan-related parameters

kvs = {}

kvs['prb'] = '../../data/17554/recon_17554_t1_probe_ave_rp.npy'

kvs['pixel'] = 55 # pixel size (um)
kvs['distance']  = 0.5 # (m)
kvs['wavelength'] = 0.083 # (nm)

# db fields, such as 'dssx', dssy', 'sclr1_ch4', 'merlin1'

kvs['x_c'] =  60
kvs['y_c'] =  66
kvs['dside'] = 100 # detector side
kvs['threshold'] = 2

kvs['outdir'] = "../../files/"


def to_sharp_bridge(header, kvs):
    
    nx = kvs['dside']
    ny = nx
    
    x0 = np.int(kvs['x_c']-nx/2)
    x1 = np.int(kvs['x_c']+nx/2)
    y0 = np.int(kvs['y_c']-ny/2)
    y1 = np.int(kvs['y_c']+ny/2)
    
    xs = []; ys = []; ics = []; ts = []; frames = []
    
    for ev in header.events(fill=True):
        xs.append(ev['data']['dssx'])
        ys.append(ev['data']['dssy'])
        ics.append(ev['data']['sclr1_ch4'])
        frame = 1.*np.fliplr(np.squeeze(np.asarray(ev['data']['merlin1'])).T)
        ts.append(frame)
        
    for i in range(0, len(ts)):
        tmp = ts[i] * ics[0] / ics[i]
        tmp = tmp[x0:x1, y0:y1]
        tmp[tmp <= kvs['threshold']] = 0.
        frames.append(tmp)
        
    sharpWriter = SharpWriter()
    sharpWriter.init(kvs['pixel'], kvs['distance'], kvs['wavelength'], kvs['dside']) 
    
    cxifile = kvs['outdir'] + "hxn" + str(kvs['sid']) + ".cxi"
    sharpWriter.write(cxifile, kvs['prb'], frames, np.asarray(xs), np.asarray(ys))

    return cxifile

print("getting and writing events...");

topic = "topic-a"
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

kvs['sid'] = sid
t1 = datetime.now();   
cxifile = to_sharp_bridge(header, kvs)
cxifile = kvs['outdir'] + "hxn" + str(kvs['sid']) + ".cxi"
producer.send(topic, pickle.dumps(cxifile))
t2 = datetime.now();
print ("processing time: ", (t2 - t1), cxifile);


