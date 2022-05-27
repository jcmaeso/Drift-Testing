from dataclasses import dataclass
import pna
import numpy as np
from scipy.io import savemat
from dataclasses import dataclass
from typing import Union
import yaml
import os
import sys 
import time

@dataclass
class Measurement_Parameters():
    mode: str
    frequency : Union[float,list]
    fi_bw : int

    def __init__(self,mode,frequency,fi_bw):
        self.mode = mode
        self.frequency = frequency
        self.fi_bw = fi_bw

def main():
    #Read input data
    input_filename = str(sys.argv[1])
    dirname = os.path.dirname(__file__)
    dirname_res = os.path.join(dirname,'Medidas')
    config = None
    with open(os.path.join(dirname_res,input_filename)) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
        config = yaml.load(file, Loader=yaml.FullLoader)
    #Start configuration
    pna_ctrl = pna.PNA_Controller("GPIB0::16::INSTR")
    pna_ctrl.multiplier_by_frequency(max(config.frequency))
    if config.mode == "monofrequency":
        pna_ctrl.setup_cut_pna_x(config.frequency,config.npoints,fi_bw=config.fi_bw)
    elif config.mode == "multifrequency":
        pna_ctrl.setup_multifreq(config.frequency,fi_bw=config.fi_bw)
        pna_ctrl.enable_fifo()
    #Performe measurement
    for i in range(0,config.npoints):
        pna_ctrl.trigger()
        print("{}/{} Measurement".format(i+1,config.npoints))
        time.sleep(config.interval*60)
    #Read data from PNA
    measure = pna_ctrl.get_data()
    np_arr = np.array(measure)
    np_arr_complex = np_arr[0:][::2]+1j*np_arr[1:][::2]
    #Reorganize in case of multifrequency for consecuitive frequencies
    if config.mode == "multifrequency":
        np_arr_complex = np.reshape(np_arr_complex,(len(config.frequency),config.npoints),order="F")
        np_arr_complex = np.transpose(np_arr_complex)
    out_filename = input_filename.split(".")[0]
    savemat(os.path.join(dirname_res,out_filename), {"data":np_arr_complex})
        


if __name__ == "__main__":
    main()