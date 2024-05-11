import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import iirfilter, lfilter

#початкові параметри
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
initial_cutoff_frequency = 5.0
initial_filter_order = 4

#генеруємо початкові дані
t = np.linspace(0, 1, 1000)

#зміння для зберігання значення шуму
noise = None

#генерація значення шуму
def generate_noise():
    global noise
    noise_mean = s_noise_mean.val
    noise_covariance = s_noise_covariance.val
    noise = noise_mean * np.random.normal(0, np.sqrt(noise_covariance), t.shape)

#оновлення графіку відповідно до змінених даних
def update_plot(val=None):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    show_noise = checkbox.get_status()[0]

    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        if noise is None:
            generate_noise()
        signal = harmonic + noise
    else:
        signal = harmonic
    
    ax.clear()
    ax.plot(t, signal, label='Гармоніка с шумом' if show_noise else 'Чиста гармоніка')
    ax.set_xlabel('Час')
    ax.set_ylabel('Сигнал')
    ax.legend()
    ax.grid(True)

    filtered_signal = filter_signal(signal)
    ax.plot(t, filtered_signal, label='Відфільтрований сигнал', color='violet')
    ax.legend()

    plt.draw()

#функція для фільтрації сигналу 
def filter_signal(signal):
    fs = 1.0 / (t[1] - t[0])
    cutoff_frequency = s_cutoff_frequency.val
    filter_order = int(s_filter_order.val)
    b, a =  iirfilter(filter_order, 2 * cutoff_frequency / fs, btype='lowpass') 
    return lfilter (b, a, signal)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.6)

ax_amplitude = plt.axes([0.15, 0.4, 0.65, 0.03])
ax_frequency = plt.axes([0.15, 0.35, 0.65, 0.03])
ax_phase = plt.axes([0.15, 0.3, 0.65, 0.03])
ax_noise_mean = plt.axes([0.15, 0.25, 0.65, 0.03])
ax_noise_covariance = plt.axes([0.15, 0.2, 0.65, 0.03])
ax_cutoff_frequency = plt.axes([0.15, 0.15, 0.65, 0.03])
ax_filter_order = plt.axes([0.15, 0.1, 0.65, 0.03])
ax_checkbox = plt.axes([0.15, 0.05, 0.2, 0.03])
ax_reset_button = plt.axes([0.4, 0.05, 0.1, 0.03])

s_amplitude = Slider(ax_amplitude, 'Амплітуда', 0.1, 10.0, valinit=initial_amplitude)
s_frequency = Slider(ax_frequency, 'Частота', 0.1, 10.0, valinit=initial_frequency)
s_phase = Slider(ax_phase, 'Фаза', 0, 2*np.pi, valinit=initial_phase)
s_noise_mean = Slider(ax_noise_mean, 'Середнє значення шуму', -1.0, 1.0, valinit=initial_noise_mean)
s_noise_covariance = Slider(ax_noise_covariance, 'Дисперсія шуму', 0.01, 1.0, valinit=initial_noise_covariance)
s_cutoff_frequency = Slider(ax_cutoff_frequency, 'Частота зрізу', 0.1, 10.0, valinit=initial_cutoff_frequency)
s_filter_order = Slider(ax_filter_order, 'Порядок фільтра', 1, 10, valinit=initial_filter_order, valstep=1)
checkbox = CheckButtons(ax_checkbox, ['Показати шум'], [True])
reset_button = Button(ax_reset_button, 'Скинути', color='lightgoldenrodyellow', hovercolor='0.975')

"""для кожного з різних груп параметрів своя функція для оновлення даних
для того, щоб шум оновлювався лише якщо середня значення шуму та дисперсії змінено"""
def update_signal(val):
    update_plot()
s_amplitude.on_changed(update_signal)
s_frequency.on_changed(update_signal)
s_phase.on_changed(update_signal)

def update_noise(val):
    generate_noise()
    update_plot()
s_noise_mean.on_changed(update_noise)
s_noise_covariance.on_changed(update_noise)

def update_filter(val):
    update_plot()
s_cutoff_frequency.on_changed(update_filter)
s_filter_order.on_changed(update_filter)

def show_noise(label):
    update_plot()
checkbox.on_clicked(show_noise)

def reset(event):
    s_amplitude.reset()
    s_frequency.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_covariance.reset()
    s_cutoff_frequency.reset()
    s_filter_order.reset()

reset_button.on_clicked(reset)

update_plot()
plt.show()
