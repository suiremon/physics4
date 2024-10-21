import numpy as np
import matplotlib.pyplot as plt
from shiny.express import input, render, ui, output

n_points = 100
ui.input_text("force_expression", label="Введите выражение для силы F(x, y): ")
ui.help_text("x+y - сложение\nx-y - вычитание\nx*y - умножение\nx/y - деление\nx//y - целочисленное деление\nx**y - степень")
ui.input_text("x_min", label="Выберите минимальный x: ")
ui.input_text("y_min", label="Выберите минимальный y: ")
ui.input_text("x_max", label="Введите максимальный x: ")
ui.input_text("y_max", label="Введите максимальный y: ")
def potential_energy(x, y, force_expression):
    F = eval(force_expression)
    return F
with ui.card(full_screen=True):
    @render.plot
    def plot():
        force_expression = input.force_expression()
        x_min = input.x_min()
        y_min = input.y_min()
        x_max = input.x_max()
        y_max = input.y_max()
        if (x_min == "" or x_max == "" or y_min == "" or y_max == ""):
            return
        x_min = float(x_min)
        x_max = float(x_max)
        y_min = float(y_min)
        y_max = float(y_max)
        if (force_expression == "" or x_max < x_min or y_max < y_min):
            return
        if (abs(x_min) > 100000 or abs(x_max) > 100000 or abs(y_min) > 100000 or abs(y_max) > 100000):
            return
        x, y = np.meshgrid(np.linspace(x_min, x_max, n_points), np.linspace(y_min, y_max, n_points))    

        z = potential_energy(x, y, force_expression)
        plt.figure(figsize=(8, 6))
        contour = plt.contourf(x, y, z, 50, cmap='YlOrRd')
        plt.colorbar(contour, label='Потенциальная энергия U(x, y)')

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Потенциальное поле')
        plt.grid(True)
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        return plt.show()
