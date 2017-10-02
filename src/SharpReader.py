from datetime import datetime

import numpy as np
import h5py

import databroker
from databroker import list_configs
from databroker import Broker

class SharpReader:

   def __init__(self):

      # frame parameters

      self.db = Broker.named('demo')
      self.x_c =  60
      self.y_c =  66
      self.nx  = 100
      self.ny  = 100
      self.threshold = 2

   def init(self, x_c, y_c, nx, ny, threshold):
      
      self.x_c =  x_c
      self.y_c =  y_c
      self.nx  =  nx
      self.ny  =  ny
      self.threshold = threshold
        
   def get_merlin1_fnames(self, sid):

      header = self.db[sid]
      df  = self.db.get_table(header,fill=False)
      
      fnames = df['merlin1'].as_matrix()
      ic = np.asarray(df['sclr1_ch4'])
    
      return fnames, ic

   def get_points(self, sid, fields):

      header = self.db[sid]
      df  = self.db.get_table(header,fill=False)
      
      x = np.array(df[fields[0]]) 
      y = np.array(df[fields[1]])
      return x,y

   def load_files(self, sid, fnames, ic):

      import filestore
      import filestore.api
      from TimepixHDF5Handler import TimepixHDF5Handler
    
      filestore.api.register_handler('TPX_HDF5', TimepixHDF5Handler, overwrite=True)

      x0 = np.int(self.x_c-self.nx/2)
      x1 = np.int(self.x_c+self.nx/2)
      y0 = np.int(self.y_c-self.ny/2)
      y1 = np.int(self.y_c+self.ny/2)

      data = []
      for i in range(0, len(fnames)):
         t = 1.*np.fliplr(np.squeeze(np.asarray(filestore.api.get_data(fnames[i]))).T)
         t = t * ic[0] / ic[i]
  
         tmp = t[x0:x1, y0:y1]
         tmp[tmp <= self.threshold] = 0.
         # data.append(np.fft.fftshift(np.sqrt(tmp)))
         data.append(tmp)

      return data


