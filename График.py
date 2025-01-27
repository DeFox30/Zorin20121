import numpy
import pylab
from matplotlib.widgets import Slider, RadioButtons, CheckButtons, Button

def gauss(sigma, mu, x):
    '''Отображаемая функция'''
    return (1.0 / (sigma * numpy.sqrt(2.0 * numpy.pi)) *
            numpy.exp(-((x - mu) ** 2) / (2 * sigma * sigma)))

def tangent_line(sigma, mu, x):
    '''Функция для вычисления значения производной и построения касательной линии'''
    y = gauss(sigma, mu, x)
    # Вычисляем производную в точке mu
    derivative = -((1.0 / (sigma * numpy.sqrt(2.0 * numpy.pi))) *
                    numpy.exp(-((mu - mu) ** 2) / (2 * sigma * sigma)) *
                    (mu - mu)) / (sigma * sigma)
    return derivative * (x - mu) + gauss(sigma, mu, mu)

# Начальные параметры
initial_sigma = 0.5
initial_mu = 0.0
sigma_range = (0.1, 1.0)
mu_range = (-4.0, 4.0)
colors = {'Красный': 'r', 'Синий': 'b', 'Зеленый': 'g'}

# Глобальные переменные
grid_visible = True
show_tangent = False  # Переменная для управления отображением касательной

# Инициализация графика
fig, graph_axes = pylab.subplots()
graph_axes.grid()
fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.55)

# Слайдер для sigma
axes_slider_sigma = pylab.axes([0.05, 0.35, 0.85, 0.04])
slider_sigma = Slider(axes_slider_sigma, label='σ', valmin=sigma_range[0], valmax=sigma_range[1], valinit=initial_sigma, valfmt='%1.2f')
slider_sigma.on_changed(lambda val: updateGraph())

# Слайдер для mu
axes_slider_mu = pylab.axes([0.05, 0.27, 0.85, 0.04])
slider_mu = Slider(axes_slider_mu, label='μ', valmin=mu_range[0], valmax=mu_range[1], valinit=initial_mu, valfmt='%1.2f')
slider_mu.on_changed(lambda val: updateGraph())

# Кнопка для изменения цвета
axes_radiobuttons = pylab.axes([0.05, 0.05, 0.2, 0.2])
radiobuttons_color = RadioButtons(axes_radiobuttons, ['Красный', 'Синий', 'Зеленый'])
radiobuttons_color.on_clicked(lambda label: updateGraph())

# Флажок для сетки
axes_checkbuttons = pylab.axes([0.35, 0.15, 0.2, 0.1])
checkbutton_grid = CheckButtons(axes_checkbuttons, ['Сетка'], [True])
checkbutton_grid.on_clicked(lambda label: onCheckClicked(label))

# Кнопка для возврата в начальное положение
axes_button_reset = pylab.axes([0.75, 0.15, 0.2, 0.05])
button_reset = Button(axes_button_reset, 'Сбросить', color='lightgoldenrodyellow', hovercolor='0.975')

# Флажок для касательной линии
axes_checkbuttons_tangent = pylab.axes([0.35, 0.05, 0.2, 0.1])
checkbutton_tangent = CheckButtons(axes_checkbuttons_tangent, ['Касательная'], [False])
checkbutton_tangent.on_clicked(lambda label: toggle_tangent(label))

# Функция обновления графика
def updateGraph():
    '''Функция для обновления графика'''
    global grid_visible
    sigma = slider_sigma.val
    mu = slider_mu.val
    x = numpy.arange(-5.0, 5.0, 0.01)
    y = gauss(sigma, mu, x)

    style = colors[radiobuttons_color.value_selected]
    graph_axes.clear()
    graph_axes.plot(x, y, style)

    if grid_visible:
        graph_axes.grid()

    graph_axes.scatter(mu, gauss(sigma, mu, mu), color='black')  # Точка на графике

    # Отображение касательной линии, если включен флажок
    if show_tangent:
        tangent_y = tangent_line(sigma, mu, x)
        graph_axes.plot(x, tangent_y, linestyle='--', color='orange', label='Касательная')
        graph_axes.legend()

    pylab.draw()

def onCheckClicked(label):
    '''Обработчик события при клике по CheckButtons'''
    global grid_visible
    if label == 'Сетка':
        grid_visible = not grid_visible
    updateGraph()

def reset(event):
    '''Сброс значений слайдеров и точки'''
    slider_sigma.set_val(initial_sigma)
    slider_mu.set_val(initial_mu)

# обработчик для кнопки сброса
button_reset.on_clicked(reset)

# Включение/выключение касательной линии
def toggle_tangent(label):
    global show_tangent
    show_tangent = not show_tangent
    updateGraph()

# Вывод графика
updateGraph()
pylab.show()