import filestore.api
from filestore.handlers import HDF5DatasetSliceHandler

class TimepixHDF5Handler(HDF5DatasetSliceHandler):
    """
    Handler for the 'AD_HDF5' spec used by Area Detectors.
    In this spec, the key (i.e., HDF5 dataset path) is always
    '/entry/detector/data'.
    Parameters
    ----------
    filename : string
        path to HDF5 file
    frame_per_point : integer, optional
        number of frames to return as one datum, default 1
    """
    _handler_name = 'TPX_HDF5'
    specs = {_handler_name}

    # TODO this is only different due to the hardcoded key being different?
    hardcoded_key = '/entry/instrument/detector/data'

    def __init__(self, filename, frame_per_point=1):
        fname = filename.replace("data", "/GPFS/CENTRAL/SHARP/data")
        super(TimepixHDF5Handler, self).__init__(
                filename=fname, key=self.hardcoded_key,
                frame_per_point=frame_per_point)

