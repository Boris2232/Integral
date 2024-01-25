import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from numpy import abs, sqrt, sin, cos, arccos, arcsin, tan, arctan, sinh, cosh, tanh, arcsinh, arctanh, round, floor, \
    ceil, exp, log, pi
import sympy as sp


class Graph:
    def __init__(self, function, left_point, right_point):
        self.function = function
        self.left_point = left_point
        self.right_point = right_point
        self.string_to_float()
        self.trap_width = 0
        self.coordinates_x = []
        self.trapezoid_area = []
        self.simpson_area = []
        self.change_to_program_code()
        self.delta_x = 0
        self.function_values = []

    def create_points_array(self, n):
        delta_x = np.divide((self.right_point - self.left_point), n)
        self.delta_x = delta_x
        left, right = self.left_point, self.right_point
        while left <= right:
            self.coordinates_x.append(left)
            left += delta_x

    def compute_trapezoid_area(self):
        self.trapezoid_area = list(map(lambda x: 2 * self.get_length(x[1]) if (
                x[0] != 0 and x[0] != len(self.coordinates_x) - 1) else self.get_length(x[1]),
                                       enumerate(self.coordinates_x)))
        return self.trapezoid_area

    def compute_simpsons_area(self):
        self.simpson_area = list(map(lambda x: self.get_length(x[1]) * 2 if (
                x[0] % 2 == 0 and x[0] != 0 and x[0] != len(self.coordinates_x) - 1) else self.get_length(
            x[1]) * 4 if (
                x[0] % 2 == 1 and x[0] != 0 and x[0] != len(self.coordinates_x) - 1) else self.get_length(x[1]),
                                     enumerate(self.coordinates_x)))
        return self.simpson_area

    def __str__(self):
        return f'Your function: {self.function}'

    def new_condition(self):
        self.function_values = []

    def change_to_program_code(self, variable=None):
        if 'np.e' not in self.function:
            self.function = self.function.replace('e', 'np.e')
        if '^' in self.function:
            self.function = self.function.replace('^', ' ** ')
        if variable:
            variable = variable.replace('^', ' ** ')
            return variable

    def get_function_value(self, point_coordinate):
        x = point_coordinate
        try:
            new_value = eval(self.function)
            self.function_values.append([x, new_value])
            return new_value
        except ZeroDivisionError or RuntimeWarning:
            return

    def save_plot(self, x, y, filename):
        step = 0.001
        left, right = self.left_point, self.right_point
        while left <= right:
            left += step
            self.get_function_value(left)
        x, y = list(map(lambda k: k[0], self.function_values)), list(map(lambda k: k[1], self.function_values))
        plt.plot(x, y)
        plt.axhline(0, color='black', linewidth=1.2)
        plt.axvline(0, color='black', linewidth=1.2)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.savefig(f'{filename}.jpg')
        plt.close()

    def get_length(self, x):
        x = x
        try:
            return eval(self.function)
        except ZeroDivisionError or RuntimeWarning:
            return

    def draw_plot(self):
        self.new_condition()
        step = 0.001
        left, right = self.left_point, self.right_point
        while left <= right:
            left += step
            self.get_function_value(left)
        x, y = list(map(lambda k: k[0], self.function_values)), list(map(lambda k: k[1], self.function_values))
        self.save_plot(x, y, filename='Function')

    def compute_area(self, height, width):
        self.down_area.append(height * width)

    def draw_trap_plot(self, traps_count):
        self.new_condition()
        self.trap_width = np.divide((self.right_point - self.left_point), traps_count)
        k_traps = 0
        left_point = self.left_point
        trap_coordinates = []
        while k_traps < traps_count:
            if k_traps != traps_count:
                width = self.trap_width
                try:
                    left_height = self.get_length(x=left_point)
                    right_height = self.get_length(x=left_point + width)
                    x_coordinates = [left_point, left_point, left_point + width, left_point + width]
                    y_coordinates = [0, left_height, right_height, 0]
                    trap_coordinates.append(
                        patches.Polygon(list(zip(x_coordinates, y_coordinates)), edgecolor='red',
                                        facecolor='none',
                                        linewidth=2))
                except ZeroDivisionError or RuntimeWarning:
                    pass
            left_point += self.delta_x
            k_traps += 1

        fig, ax = plt.subplots()
        for i in trap_coordinates:
            ax.add_patch(i)
        self.save_plot(None,None,filename='Trapezoidal_area')

    def string_to_float(self):
        self.left_point = self.change_to_program_code(variable=self.left_point)
        self.right_point = self.change_to_program_code(variable=self.right_point)
        if 'pi' in self.right_point:
            new_var = self.right_point.replace('pi', 'np.pi')
            self.right_point = eval(new_var, {"np": np})
        elif 'e' in self.right_point:
            new_var = self.right_point.replace('e', 'np.e')
            self.right_point = eval(new_var, {"np": np})
        if 'pi' in self.left_point:
            new_var = self.left_point.replace('pi', 'np.pi')
            self.left_point = eval(new_var, {"np": np})
        elif 'e' in self.left_point:
            new_var = self.left_point.replace('e', 'np.e')
            self.left_point = eval(new_var, {"np": np})
        self.right_point = float(self.right_point)
        self.left_point = float(self.left_point)

    def compute_simpsons_error(self, traps_count):
        borders = (self.right_point - self.left_point) ** 5
        denominator = 180 * (traps_count ** 4)
        find_max_ = list(enumerate(list(map(lambda x: self.get_length(x[1]), enumerate(self.coordinates_x)))))
        find_max = self.coordinates_x[max(find_max_, key=lambda x: x[1])[0]]
        x = sp.Symbol('x')
        forth_der = sp.diff(self.function, x, 4)
        value = forth_der.subs(x, find_max)
        return (value * borders) / denominator

    def compute_trapezoid_error(self,traps_count):
        borders = (self.right_point - self.left_point) ** 3
        denominator = 12 * (traps_count ** 2)
        find_max_ = list(enumerate(list(map(lambda x: self.get_length(x[1]), enumerate(self.coordinates_x)))))
        find_max = self.coordinates_x[max(find_max_, key=lambda x: x[1])[0]]
        x = sp.Symbol('x')
        forth_der = sp.diff(self.function, x, 2)
        value = forth_der.subs(x, find_max)
        return (value * borders) / denominator


a = input('Enter your function : ')
l = str(input("Left point of Domain : "))
r = str(input("Right point of Domain : "))
graph = Graph(a, l, r)
print(graph)
graph.draw_plot()
traps_count = int(input('Enter the number of traps : '))
graph.create_points_array(traps_count)
print(f'Trapezoidal area of the graph : {(sum(graph.compute_trapezoid_area())) * (graph.delta_x / 2)}')
print(f'Simpsons area of the graph : {(sum(graph.compute_simpsons_area()) * (graph.delta_x / 3))}')
graph.draw_trap_plot(traps_count=traps_count)
error_T = graph.compute_trapezoid_error(traps_count)
print(f'Trapezoidal estimated error = {error_T}')
error_s = graph.compute_simpsons_error(traps_count)
print(f'Simpsons estimated error = {error_s}')
