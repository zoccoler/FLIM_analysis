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