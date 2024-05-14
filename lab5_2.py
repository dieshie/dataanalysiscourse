import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Slider, Toggle, Button, ColorPicker
from bokeh.plotting import figure
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

plot = figure(
    height=800, width=800, title='Графіки',
    tools="crosshair, pan, reset, save, wheel_zoom",
    x_range=[0, 1],
    y_range=[-1, 1],
    sizing_mode="scale_both"
    )

harmonic_source = ColumnDataSource(data=dict(x=t, y=t)) 
filtered_source = ColumnDataSource(data=dict(x=t, y=t))

line = plot.line('x', 'y', name="Гapмонікa з шумом", source=harmonic_source, line_width=3, line_alpha=0.6, line_color="black")
plot.line('x', 'y', name="Відфільтрований сигнал", source=filtered_source, line_width=3, line_alpha=0.6, line_color="violet")

#генерація значення шуму
def generate_noise():
    global noise
    noise_mean = s_noise_mean.value
    noise_covariance = s_noise_covariance.value
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), t.shape)

#оновлення графіку відповідно до змінених даних
def update_plot(attr, old, new):
    amplitude = s_amplitude.value
    frequency = s_frequency.value
    phase = s_phase.value

    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)

    if check_show_noise.active:
        if noise is None:
            generate_noise()
        signal = harmonic + noise
    else:
        signal = harmonic
    
    plot.y_range.start = -amplitude
    plot.y_range.end = amplitude

    harmonic_source.data = dict(x=t, y=signal)
    filtered_source.data = dict(x=t, y=filter_signal(signal))

#функція для фільтрації сигналу(фільтр з минулого пункту)
def filter_signal(signal):
    fs = 1.0 / (t[1] - t[0])
    cutoff_frequency = s_cutoff_frequency.value
    filter_order = int(s_filter_order.value)
    b, a =  iirfilter(filter_order, 2 * cutoff_frequency / fs, btype='lowpass') 
    return lfilter (b, a, signal)

def update_noise(attr, old, new):
    generate_noise()
    update_plot(None, None, None)

def reset_values():
    s_amplitude.value = initial_amplitude
    s_frequency.value =initial_frequency
    s_phase.value = initial_phase
    s_noise_mean.value = initial_noise_mean
    s_noise_covariance.value = initial_noise_covariance
    s_cutoff_frequency.value = initial_cutoff_frequency
    s_filter_order.value = initial_filter_order
    check_show_noise.active = False

s_amplitude = Slider (title='Aмплiтyдa', start=0.1, end=10.0, value=initial_amplitude, step=0.05)
s_frequency = Slider (title='Частота', start=0.1, end=10.0, value=initial_frequency, step=0.05)
s_phase = Slider (title='Фаза', start=0, end= 2 * np.pi, value=initial_phase, step=0.05)
s_noise_mean = Slider (title='Середнє значення шуму', start=-1.0, end=1.0, value=initial_noise_mean, step=0.05)
s_noise_covariance = Slider (title='Дисперсія шумy', start=0.0, end=0.5, value=initial_noise_covariance, step=0.025)
s_cutoff_frequency = Slider (title='Чacтoта зpiзy', start=0.1, end=50.0, value=initial_cutoff_frequency, step=0.05)
s_filter_order = Slider (title='Пopядок фільтру', start=1, end=10, value=initial_filter_order, step=1)

picker = ColorPicker(title="Колір графіку з шумом")
picker.js_link('color', line.glyph, 'line_color')

check_show_noise = Toggle(label="Показати шум", button_type="success")

reset_button = Button(label="Скинути", button_type="warning")
reset_button.on_click(reset_values)

widgets = (s_amplitude, s_frequency, s_phase, s_cutoff_frequency, s_filter_order)
for widget in widgets:
    widget.on_change('value', update_plot)

s_noise_mean.on_change('value', update_noise)
s_noise_covariance.on_change('value', update_noise)

check_show_noise.on_change("active", update_plot)

inputs = column(*widgets, s_noise_mean, s_noise_covariance, check_show_noise, reset_button, picker)
layout = column(plot, inputs, sizing_mode="scale_both")
update_plot(None, None, None)

curdoc().title = "Lab5"
curdoc().add_root(layout)