import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import iirfilter, filtfilt

x = np.linspace(0, 10, 1000)
noise_enabled = [True]
filter_enabled = [True]
noise = np.zeros_like(x)

params = {
    "amp": 1.0,
    "freq": 1.0,
    "phase": 0.0,
    "noise_mean": 0.0,
    "noise_cov": 0.2,
    "cutoff": 5.0
}


def generate_clean():
    return params["amp"] * np.sin(2 * np.pi * params["freq"] * x + params["phase"])

def generate_noise():
    return np.random.normal(params["noise_mean"], params["noise_cov"], len(x))

def apply_filter(signal):
    b, a = iirfilter(
        N=4,
        Wn=params["cutoff"],
        btype='low',
        ftype='butter',
        fs=100 
    )
    return filtfilt(b, a, signal)



fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.45)
ax.set_ylim(-2, 2)

line_clean, = ax.plot(x, generate_clean(), 'b--', label='Signal')
line_noisy, = ax.plot(x, generate_clean(), 'orange', label='Noisy', alpha=0.7)
line_filtered, = ax.plot(x, generate_clean(), 'purple', label='Filtered')
ax.legend(loc="upper right", bbox_to_anchor=(1, 1))


def update_signal(val=None):
    clean = generate_clean()
    line_clean.set_ydata(clean)
    if noise_enabled[0]:
        line_noisy.set_ydata(clean + noise)
        line_filtered.set_ydata(apply_filter(clean + noise))
    fig.canvas.draw_idle()

def refresh_noise():
    global noise
    noise = generate_noise()
    update_signal()


def create_slider(axpos, label, valmin, valmax, valinit, callback):
    ax_slider = plt.axes(axpos)
    slider = Slider(ax_slider, label, valmin, valmax, valinit=valinit)
    slider.on_changed(callback)
    return slider

sliders = {
    "amp": create_slider([0.25, 0.38, 0.65, 0.03], 'Amplitude', 0.0, 2.0, params["amp"],
                         lambda v: update_param("amp", v)),
    "freq": create_slider([0.25, 0.34, 0.65, 0.03], 'Frequency', 0.1, 5.0, params["freq"],
                          lambda v: update_param("freq", v)),
    "phase": create_slider([0.25, 0.30, 0.65, 0.03], 'Phase', 0.0, 2*np.pi, params["phase"],
                           lambda v: update_param("phase", v)),
    "noise_mean": create_slider([0.25, 0.26, 0.65, 0.03], 'Noise Mean', -1.0, 1.0, params["noise_mean"],
                                lambda v: update_param("noise_mean", v, noise=True)),
    "noise_cov": create_slider([0.25, 0.22, 0.65, 0.03], 'Noise Covariance', 0.0, 1.0, params["noise_cov"],
                               lambda v: update_param("noise_cov", v, noise=True)),
    "cutoff": create_slider([0.25, 0.18, 0.65, 0.03], 'Cutoff Frequency', 1.0, 10.0, params["cutoff"],
                            lambda v: update_param("cutoff", v))
}

def update_param(name, value, noise=False):
    params[name] = value
    if noise:
        refresh_noise()
    else:
        update_signal()


reset_ax = plt.axes([0.25, 0.08, 0.1, 0.04])
button = Button(reset_ax, 'Reset')
def reset(event):
    for key, slider in sliders.items():
        slider.reset()
    refresh_noise()
button.on_clicked(reset)

check_ax = plt.axes([0.7, 0.05, 0.17, 0.1])
check = CheckButtons(check_ax, ['Show Noise'], [True])

filter_check_ax = plt.axes([0.5, 0.05, 0.20, 0.1])
filter_check = CheckButtons(filter_check_ax, ['Show Filtered'], [True])
def toggle_noise(label):
    noise_enabled[0] = not noise_enabled[0]
    line_noisy.set_visible(noise_enabled[0])
    line_filtered.set_visible(noise_enabled[0])
    refresh_noise() if noise_enabled[0] else update_signal()

def toggle_filtered(label):
    filter_enabled[0] = not filter_enabled[0]
    line_filtered.set_visible(filter_enabled[0])
    update_signal()

check.on_clicked(toggle_noise)
filter_check.on_clicked(toggle_filtered)

refresh_noise()
plt.show()
