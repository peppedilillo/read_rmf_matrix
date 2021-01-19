import numpy as np
from astropy.io import fits

def read_rmf_matrix(rmf_file):
    '''
    Read a rmf fits built according to (OGIP Calibration Memo CAL/GEN/92-002, George, I.M. 1992)
    OGIP standard and returns a numpy array of the redistribution matrix.
    
    par rmf_file: str
    return m: numpy array
    '''
    (data, header) = fits.getdata(rmf_file, 'MATRIX', header=True)
    CH_NUM = header['DETCHANS']
    m = np.zeros((CH_NUM,CH_NUM))
    for row in range(CH_NUM):
        N_GRP, MAT = data[row][2],  data[row][-1]
        F_CHAN, N_CHAN = tuple(map(lambda x: x[:N_GRP], data[row][3:-1]))
        for i, (f_chan, n_chan) in enumerate(zip(F_CHAN, N_CHAN)):
            m[row,f_chan:f_chan + n_chan] = MAT[:n_chan]
            MAT = np.delete(MAT,np.s_[:n_chan])
    return m