def create_time_array(frequency, n_points=100):
    '''
    Create time array from laser frequency
    
    Parameters
    ----------
    frequency: float
        Frquency of the pulsed laser (in MHz)
    n_points: int, optional
        The number of samples collected between each aser shooting
    Returns
    -------
    time_array : array
        Time array (in nanoseconds)
    '''
    import numpy as np
    time_window = 1 / (frequency * 10**6)
    time_window_ns = time_window * 10**9 # in nanoseconds
    time_step = time_window_ns / n_points # ns
    array = np.arange(0, n_points)
    time_array = array * time_step
    return time_array

def monoexp(x, A, tau):
    import numpy as np
    return A * np.exp(-(1/tau)*x)

def make_synthetic_flim_data(time_array, amplitude_list, tau_list):
    """
    Create a synthetic FLIM image from amplitudes and tau
    
    Each different tau in the list adds a new pixel to the image
    """
    import numpy as np
    # Handle input types
    if not isinstance(tau_list, list):
        tau_list = [tau_list]
    if not isinstance(amplitude_list, list):
        amplitude_list = [amplitude_list]
    if len(amplitude_list)==1 and len(amplitude_list)<len(tau_list):
        amplitude_list = [amplitude_list] * len(tau_list)
    # Generates synthetic image
    flim_data_list = []
    for amp, tau in zip(amplitude_list, tau_list):
        intensity = monoexp(time_array, amp, tau)
        flim_data = np.repeat(intensity[:, np.newaxis], 1, axis=1).reshape(len(time_array), 1,1)
        flim_data_list.append(flim_data)
    flim_data = np.concatenate(flim_data_list, axis=1)
    return flim_data

def get_phasor_components(flim_data, harmonic=1):
    '''
    Calculate phasor components G and S from the fourier transform
    
    The index of the Fourier transform corresponds to the harmonic
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
    return g, s


def add_phasor_circle(ax):
    '''
    Generate FLIM universal semi-circle plot
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    angles = np.linspace(0, np.pi, 180)
    x =(np.cos(angles) + 1) / 2
    y = np.sin(angles) / 2
    ax.plot(x,y, 'gray', alpha=0.3)
    return ax

def add_tau_lines(ax, tau_list, frequency):
    import numpy as np
    import matplotlib.pyplot as plt
    if not isinstance(tau_list, list):
        tau_list = [tau_list]
    frequency = frequency * 1E6 # MHz to Hz
    w = 2*np.pi*frequency # Hz to radians/s
    for tau in tau_list:
        tau = tau * 1E-9 # nanoseconds to seconds
        g = 1 / ( 1 + ( (w * tau)**2) )
        s = (w * tau) / ( 1 + ( (w * tau)**2) )
        dot, = ax.plot(g, s, marker='o', mfc='none')
        array = np.linspace(0, g, 50)
        y = (array*s/g)
        ax.plot(array, y, color = dot.get_color())