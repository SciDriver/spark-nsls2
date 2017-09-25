from datetime import datetime

import numpy as np
import h5py
from scipy import interpolate

class SharpWriter:

   def __init__(self):

      self.ccd_pixel_um = 55    # detector pixel size (um)
      self.z_m          = 0.76  # detector-to-sample distance (m)
      self.lambda_nm    = 0.155 # x-ray wavelength (nm)
      self.det_side     = 128

      self.real_translation = []
      self.corner_pos = []
      
      self.init_obj = []
      self.init_prb = []

      self.frames = []
      self.emptyFrames = []

   def init(self, ccd_pixel_um, z_m, lambda_nm, det_side):
      
      self.ccd_pixel_um = ccd_pixel_um
      self.z_m          = z_m
      self.lambda_nm    = lambda_nm
      self.det_side     = det_side

   def set_frames(self, dbFrames):

      nz  = len(dbFrames)

      self.frames = []
      self.emptyFrames = []
      for i in range(0, nz):
         if np.sum(dbFrames[i]) > 0.:
            self.frames.append(dbFrames[i])
            # frames.append(np.fft.fftshift(dbFrames[i]**2))
         else :
            self.emptyFrames.append(i)
      
      return self.emptyFrames

   def set_points(self, xs, ys):

      real_pixel_size =  self.z_m*self.lambda_nm*1e-3/(self.det_side*self.ccd_pixel_um)

      x_real_space_pixel_um = real_pixel_size*1.e6
      y_real_space_pixel_um = real_pixel_size*1.e6

      p_ssx_pixel = np.round(xs / x_real_space_pixel_um)
      p_ssy_pixel = np.round(ys / y_real_space_pixel_um)

      X = np.delete(p_ssx_pixel, self.emptyFrames)
      Y = np.delete(p_ssy_pixel, self.emptyFrames)

      X -= min(X)
      Y -= min(Y)

      # transpose X and Y for the input file
      # pixel_translation = np.column_stack((X, Y, np.zeros(Y.size)))
       
      pixel_translation = np.column_stack((Y, X, np.zeros(Y.size)))
      self.real_translation = pixel_translation * real_pixel_size
       
      nx_obj = int(self.det_side + np.max(X) - np.min(X))
      ny_obj = int(self.det_side + np.max(Y) - np.min(Y))

      self.init_obj = np.random.uniform(0, 0.5, (nx_obj, ny_obj)) \
                      * np.exp(np.random.uniform(0, 0.5, (nx_obj, ny_obj))*1.j)

      return X, Y

   def congrid(self, array_in, shape):
      
      x_in,y_in = np.shape(array_in)
      x = np.arange(x_in)
      y = np.arange(y_in)

      kernel = interpolate.RectBivariateSpline(x,y,array_in, kx=2,ky=2)
      xx = np.linspace(x.min(),x.max(),shape[0])
      yy = np.linspace(y.min(),y.max(),shape[1])

      return  kernel(xx,yy)

   def set_probe(self, prbfile):

      probe = np.load(prbfile)

      init_prb_flag = False  #False to load a pre-existing array
      self.init_prb = probe

      nx = self.det_side
      ny = self.det_side

      if self.init_prb.shape != (nx, ny):
         print('Resizing loaded probe from %s to %s' % (init_prb.shape, (nx, ny)))
         amp = congrid(np.abs(self.init_prb), (nx, ny))
         pha = congrid(np.angle(self.init_prb), (nx, ny))
         self.init_prb = amp * np.exp(1j * pha)

      return self.init_prb

   def write_file(self, cxifile):

       det_pixel_size = self.ccd_pixel_um*1e-6

       energyJ = 1.98644e-16/self.lambda_nm # in J
       self.corner_pos = [self.det_side/2*self.ccd_pixel_um*1e-6, self.det_side/2*self.ccd_pixel_um*1e-6, self.z_m]

       # Write out input file

       f = h5py.File(cxifile, "w")
       f.create_dataset("cxi_version",data=140)
       entry_1 = f.create_group("entry_1")

       # 1. sample_1: name, geometry_1

       sample_1   = entry_1.create_group("sample_1")

       # 1.1 geometry_1: translation:

       geometry_1 = sample_1.create_group("geometry_1")
       geometry_1.create_dataset("translation", data=self.real_translation) # in meters

       # 2. instrument_1: detector_1, source_1, data_1

       instrument_1 = entry_1.create_group("instrument_1")

       # 2.1 detector_1: distance, corner_position, x_pixel_size, y_pixel_size
       # translation, data and axes, probe_mask

       detector_1 = instrument_1.create_group("detector_1")
       detector_1.create_dataset("distance", data=self.z_m) # in meters
       detector_1.create_dataset("corner_position", data=self.corner_pos) # in meters
       detector_1.create_dataset("x_pixel_size", data=det_pixel_size) # in meters
       detector_1.create_dataset("y_pixel_size", data=det_pixel_size) # in meters

       detector_1["translation"] = h5py.SoftLink('/entry_1/sample_1/geometry_1/translation')

       data = detector_1.create_dataset("data",data=self.frames)
       data.attrs['axes'] = "translation:y:x"

       detector_1.create_dataset("initial_image",data=self.init_obj)

       # 2.2 source_1: energy

       source_1 = instrument_1.create_group("source_1")
       source_1.create_dataset("energy", data=energyJ) # in J
       source_1.create_dataset("illumination", data=self.init_prb)
       source_1['probe'] = h5py.SoftLink('/entry_1/instrument_1/source_1/illumination')

       # 2.3 data_1: data, translation

       data_1 = entry_1.create_group("data_1")

       data_1["data"] = h5py.SoftLink('/entry_1/instrument_1/detector_1/data')
       data_1["translation"] = h5py.SoftLink('/entry_1/sample_1/geometry_1/translation')

       f.close()

   def write(self, cxifile, prbfile, frames, xs, ys):

      emptyFrames = self.set_frames(frames)
      X, Y = self.set_points(xs, ys)
      prb = self.set_probe(prbfile)
      self.write_file(cxifile)



   
    
 
