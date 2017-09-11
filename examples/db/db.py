#!/usr/bin/env python

from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import h5py
from scipy import interpolate

# from hxntools.handlers import register
# register()

def get_fnames():

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

print("getting fnames from db ...");
t1 = datetime.now();
fnames = get_fnames()
t2 = datetime.now();
print ("processing time: ", (t2 - t1), ", fnames: ", len(fnames));

print("loading files ...");
t1 = datetime.now();
num_frames = load_files(fnames)
t2 = datetime.now();
print ("processing time: ", (t2 - t1), "num_frames: ", num_frames);
