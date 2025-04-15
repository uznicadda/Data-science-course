import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons

x = np.linspace(0, 10, 1000)
noise_enabled = [True]
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


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.45)
ax.set_ylim(-2, 2)

line_clean, = ax.plot(x, generate_clean(), 'b--', label='Signal')
line_noisy, = ax.plot(x, generate_clean(), 'orange', label='Noisy', alpha=0.7)
ax.legend(loc="upper right", bbox_to_anchor=(1, 1))


def update_signal(val=None):
    clean = generate_clean()
    line_clean.set_ydata(clean)
    if noise_enabled[0]:
        line_noisy.set_ydata(clean + noise)
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
                               lambda v: update_param("noise_cov", v, noise=True))
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

check_ax = plt.axes([0.8, 0.05, 0.15, 0.1])
check = CheckButtons(check_ax, ['Show Noise'], [True])
def toggle_noise(label):
    noise_enabled[0] = not noise_enabled[0]
    line_noisy.set_visible(noise_enabled[0])
    refresh_noise() if noise_enabled[0] else update_signal()
check.on_clicked(toggle_noise)

refresh_noise()
plt.show()
