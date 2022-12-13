def get_phasor_components(flim_data, harmonic=1):
    '''
    Calculate phasor components G and S from the fourier transform
    '''
    import numpy as np
    flim_data_fft = np.fft.fft(flim_data, axis=0)
    dc = flim_data_fft[0].real
    # change the zeros to the img average
    # dc = np.where(dc != 0, dc, int(np.mean(dc)))
    dc = np.where(dc != 0, dc, 1)
    g = flim_data_fft[harmonic].real
    g = g / dc
    s = abs(flim_data_fft[harmonic].imag)
    s /= dc
    return g, s, dc

