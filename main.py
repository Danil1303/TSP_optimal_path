import sys
import math
import functions
from time import sleep
from classes import Point
from copy import deepcopy
from PyQt5.QtCore import Qt, QPoint, QThread
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit, QMainWindow


class MainWindow(QMainWindow):
    window_width = 1920
    window_height = 1000

    def __init__(self):
        QMainWindow.__init__(self)

        self.setFixedSize(MainWindow.window_width, MainWindow.window_height)
        # self.setMinimumSize(self.window_width, self.window_height)
        self.setMouseTracking(True)

        self.working_field = QPixmap(MainWindow.window_width - 250, MainWindow.window_height)
        self.working_field.fill(Qt.white)
        self.mouse_coordinates = QPoint()

        self.painter = QPainter(self.working_field)
        self.painter.setBrush(Qt.white)

        self.clear_button = QPushButton(self)
        self.clear_button.setText('Очистить')
        self.clear_button.setGeometry(MainWindow.window_width - 240, MainWindow.window_height - 45, 80, 30)
        self.clear_button.clicked.connect(self.clear_working_field)

        self.button_greedy = QPushButton(self)
        self.button_greedy.setText('Жадный алгоритм')
        self.button_greedy.setGeometry(MainWindow.window_width - 240, 15, 120, 30)
        self.button_greedy.clicked.connect(self.call_greedy_algorithm)

        self.line_edit_greedy_result = QLineEdit(self)
        self.line_edit_greedy_result.setGeometry(MainWindow.window_width - 240, 50, 220, 30)
        self.line_edit_greedy_result.setEnabled(False)

        self.button_ant = QPushButton(self)
        self.button_ant.setText('Роевой алгоритм')
        self.button_ant.setGeometry(MainWindow.window_width - 240, 100, 120, 30)
        self.button_ant.clicked.connect(self.call_ant_algorithm)

        self.label_ant_iterations = QLabel(self)
        self.label_ant_iterations.move(MainWindow.window_width - 240, 135)
        self.label_ant_iterations.setText('Количество итераций:')
        self.label_ant_iterations.adjustSize()

        self.label_ant_distance_value = QLabel(self)
        self.label_ant_distance_value.move(MainWindow.window_width - 240, 155)
        self.label_ant_distance_value.setText('Степень влияния расстояния:')
        self.label_ant_distance_value.adjustSize()

        self.label_ant_pheromone_value = QLabel(self)
        self.label_ant_pheromone_value.move(MainWindow.window_width - 240, 175)
        self.label_ant_pheromone_value.setText('Степень влияния феромона:')
        self.label_ant_pheromone_value.adjustSize()

        self.label_ant_evaporation_coefficient = QLabel(self)
        self.label_ant_evaporation_coefficient.move(MainWindow.window_width - 240, 195)
        self.label_ant_evaporation_coefficient.setText('Коэффициент испарения:')
        self.label_ant_evaporation_coefficient.adjustSize()

        self.label_ant_pheromone_value = QLabel(self)
        self.label_ant_pheromone_value.move(MainWindow.window_width - 240, 215)
        self.label_ant_pheromone_value.setText('Запас феромона у муравья:')
        self.label_ant_pheromone_value.adjustSize()

        self.line_edit_ant_iterations = QLineEdit(self)
        self.line_edit_ant_iterations.setGeometry(MainWindow.window_width - 50, 133, 30, 20)
        self.line_edit_ant_iterations.setText('50')

        self.line_edit_ant_distance_value = QLineEdit(self)
        self.line_edit_ant_distance_value.setGeometry(MainWindow.window_width - 50, 153, 30, 20)
        self.line_edit_ant_distance_value.setText('1')

        self.line_edit_ant_pheromone_value = QLineEdit(self)
        self.line_edit_ant_pheromone_value.setGeometry(MainWindow.window_width - 50, 173, 30, 20)
        self.line_edit_ant_pheromone_value.setText('1')

        self.line_edit_ant_evaporation_coefficient = QLineEdit(self)
        self.line_edit_ant_evaporation_coefficient.setGeometry(MainWindow.window_width - 50, 193, 30, 20)
        self.line_edit_ant_evaporation_coefficient.setText('0.2')

        self.line_edit_ant_pheromone_value = QLineEdit(self)
        self.line_edit_ant_pheromone_value.setGeometry(MainWindow.window_width - 50, 213, 30, 20)
        self.line_edit_ant_pheromone_value.setText('20')

        self.line_edit_ant_result = QLineEdit(self)
        self.line_edit_ant_result.setGeometry(MainWindow.window_width - 240, 240, 220, 30)
        self.line_edit_ant_result.setEnabled(False)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.working_field)

    def mousePressEvent(self, event) -> None:
        x_coordinate, y_coordinate = event.pos().x(), event.pos().y()
        if event.button() & Qt.LeftButton:
            if MainWindow.check_borders(x_coordinate, y_coordinate) and MainWindow.check_collisions(x_coordinate,
                                                                                                    y_coordinate):
                self.painter.setPen(Qt.blue)
                self.draw_point(x_coordinate, y_coordinate, point_number=Point.point_number)
                Point(x_coordinate, y_coordinate)
                self.update()

    @staticmethod
    def check_borders(x_coordinate: int, y_coordinate: int) -> bool:
        if x_coordinate > 15:
            if x_coordinate < MainWindow.window_width - 250 - 15:
                if y_coordinate > 15:
                    if y_coordinate < MainWindow.window_height - 15:
                        return True

    @staticmethod
    def check_collisions(x_coordinate: int, y_coordinate: int) -> bool:
        if Point.points_dict != 0:
            for point in Point.points_dict.values():
                if math.sqrt((x_coordinate - point.point_x) ** 2 + (y_coordinate - point.point_y) ** 2) < 100:
                    return False
            return True

    def clear_working_field(self) -> None:
        Point.delete_points()
        self.working_field.fill(Qt.white)
        self.update()

    @staticmethod
    def create_graph() -> dict[int, list[list[int], list[float]]]:
        graph = {}
        for point_number, point in Point.points_dict.items():
            graph[point_number] = [[], []]
            for destination_point_number, destination_point in Point.points_dict.items():
                if destination_point_number != 1 and point is not destination_point:
                    graph[point_number][0].append(destination_point_number)
                    graph[point_number][1].append(math.sqrt((point.point_x - destination_point.point_x) ** 2 + (
                            point.point_y - destination_point.point_y) ** 2))
        return graph

    def call_greedy_algorithm(self) -> None:
        self.working_field.fill(Qt.white)
        total_way, order_list = functions.greedy(MainWindow.create_graph())

        self.painter.setPen(QPen(Qt.black, 5))
        for i in range(len(order_list) - 1):
            self.draw_path(order_list[i], order_list[i + 1])
        self.painter.setPen(Qt.black)
        for point_number, point in Point.points_dict.items():
            self.draw_point(point.point_x, point.point_y, point_number)
        self.update()
        self.line_edit_greedy_result.setText(str(total_way))

    def call_ant_algorithm(self) -> None:
        iterations = int(self.line_edit_ant_iterations.text())
        alpha = float(self.line_edit_ant_distance_value.text())
        beta = float(self.line_edit_ant_pheromone_value.text())
        evaporation_coefficient = 1 - float(self.line_edit_ant_evaporation_coefficient.text())
        pheromone_value = float(self.line_edit_ant_pheromone_value.text())

        def draw_ant():
            self.block_interface()
            for step in functions.ant_algorithm(MainWindow.create_graph(), iterations, alpha, beta,
                                                evaporation_coefficient, pheromone_value):
                # Отрисовка всех путей
                self.working_field.fill(Qt.white)
                for start_point, values in step.items():
                    for i, destination_point in enumerate(values[0]):
                        self.painter.setPen(QPen(Qt.gray, self.calculate_line_thickness(values[2][i])))
                        self.draw_path(start_point, destination_point)
                # Отрисовка оптимального пути на данной итерации
                current_optimal_route = functions.ant_local_optimal_path(deepcopy(step))
                for i in range(len(current_optimal_route[1]) - 1):
                    self.painter.setPen(QPen(Qt.black, self.calculate_line_thickness(current_optimal_route[2][i]) + 1))
                    self.draw_path(current_optimal_route[1][i], current_optimal_route[1][i + 1])
                self.line_edit_ant_result.setText(str(current_optimal_route[0]))
                self.painter.setPen(Qt.black)
                for point_number, point in Point.points_dict.items():
                    self.draw_point(point.point_x, point.point_y, point_number)
                self.update()
                sleep(0.05)
            self.unlock_interface()

        self.thread_ant = ThreadAnt(draw_ant)
        self.thread_ant.start()

    def draw_point(self, x_coordinate: int, y_coordinate: int, point_number: int):
        self.painter.drawEllipse(x_coordinate - 15, y_coordinate - 15, 30, 30)
        if point_number < 10:
            self.painter.drawText(x_coordinate - 3, y_coordinate + 4, str(point_number))
        elif point_number < 100:
            self.painter.drawText(x_coordinate - 6, y_coordinate + 4, str(point_number))
        else:
            self.painter.drawText(x_coordinate - 10, y_coordinate + 4, str(point_number))

    def draw_path(self, start_point: int, end_point: int) -> None:
        start_x, start_y = Point.points_dict[start_point].point_x, Point.points_dict[start_point].point_y
        end_x, end_y = Point.points_dict[end_point].point_x, Point.points_dict[end_point].point_y
        self.painter.drawLine(start_x, start_y, end_x, end_y)

    @staticmethod
    def calculate_line_thickness(weight: float) -> float:
        line_thickness = weight * 30
        if line_thickness > 21:
            line_thickness = 21
        return line_thickness

    def block_interface(self) -> None:
        self.button_greedy.setEnabled(False)
        self.button_ant.setEnabled(False)
        self.clear_button.setEnabled(False)

    def unlock_interface(self) -> None:
        self.button_greedy.setEnabled(True)
        self.button_ant.setEnabled(True)
        self.clear_button.setEnabled(True)


class ThreadAnt(QThread):

    def __init__(self, draw_ant: functions):
        QThread.__init__(self)
        self.threading_function = draw_ant

    def run(self) -> None:
        self.threading_function()


def optimal_path():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    optimal_path()

# pyinstaller -w -F --onefile --upx-dir=D:\UPX main.py
