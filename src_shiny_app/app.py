import numpy as np
import matplotlib.pyplot as plt
import sympy as sp  # Для символьных вычислений (интегралов)
from shiny.express import input, render, ui, output

n_points = 100

# Интерфейс для ввода пользователем
ui.input_text("force_expression", label="Введите выражение для силы F(x, y): ")
ui.help_text("x+y - сложение\nx-y - вычитание\nx*y - умножение\nx/y - деление\nx//y - целочисленное деление\nx**y - степень")
ui.input_text("x_min", label="Выберите минимальный x: ")
ui.input_text("y_min", label="Выберите минимальный y: ")
ui.input_text("x_max", label="Введите максимальный x: ")
ui.input_text("y_max", label="Введите максимальный y: ")

# Функция для нахождения потенциальной энергии через интегрирование
def potential_energy(x, y, force_expression):
    # Символьные переменные
    x_sym, y_sym = sp.symbols('x y')
    
    # Интерпретируем введенное выражение силы как функцию
    F = eval(force_expression, {"x": x_sym, "y": y_sym})
    
    # Находим компоненты силы через частные производные
    F_x = sp.diff(F, x_sym)  # Частная производная силы по x
    F_y = sp.diff(F, y_sym)  # Частная производная силы по y
    
    # Интегрируем для нахождения потенциальной энергии
    U_x = sp.integrate(-F_x, x_sym)  # Интеграл компоненты силы по x
    U_y = sp.integrate(-F_y, y_sym)  # Интеграл компоненты силы по y
    
    # Общая потенциальная энергия - сумма интегралов
    U = U_x + U_y
    
    # Превращаем выражение в числовую функцию для дальнейших вычислений
    U_func = sp.lambdify((x_sym, y_sym), U, "numpy")
    
    return U_func(x, y)

with ui.card(full_screen=True):
    @render.plot
    def plot():
        force_expression = input.force_expression()
        x_min = input.x_min()
        y_min = input.y_min()
        x_max = input.x_max()
        y_max = input.y_max()
        
        # Проверка на корректность введенных данных
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
        
        # Создаем сетку координат
        x, y = np.meshgrid(np.linspace(x_min, x_max, n_points), np.linspace(y_min, y_max, n_points))
        
        # Вычисляем потенциальную энергию
        z = potential_energy(x, y, force_expression)
        
        # Визуализируем потенциальное поле
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

