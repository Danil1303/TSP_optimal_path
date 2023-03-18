import sys
import math
import functions
from time import sleep
from classes import Point
from PyQt5.QtCore import Qt, QPoint, QThread
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit, QWidget


class MainWindow(QWidget):
    window_width = 920
    window_height = 500

    def __init__(self):
        super(MainWindow, self).__init__()
        super().__init__()

        self.setFixedSize(MainWindow.window_width, MainWindow.window_height)
        # self.setMinimumSize(self.window_width, self.window_height)
        self.setMouseTracking(True)

        self.working_field = QPixmap(MainWindow.window_width - 150, MainWindow.window_height)
        self.working_field.fill(Qt.white)
        self.mouse_coordinates = QPoint()

        self.painter = QPainter(self.working_field)
        self.painter.setBrush(Qt.white)

        self.clear_button = QPushButton(self)
        self.clear_button.setText('Очистить')
        self.clear_button.setGeometry(MainWindow.window_width - 140, MainWindow.window_height - 45, 80, 30)
        self.clear_button.clicked.connect(self.clear_working_field)

        self.greedy_button = QPushButton(self)
        self.greedy_button.setText('Жадный алгоритм')
        self.greedy_button.setGeometry(MainWindow.window_width - 140, 15, 120, 30)
        self.greedy_button.clicked.connect(self.calculate_greedy_algorithm)

        self.greedy_edit = QLineEdit(self)
        self.greedy_edit.setGeometry(MainWindow.window_width - 140, 50, 100, 30)
        self.greedy_edit.setEnabled(False)

        self.ant_button = QPushButton(self)
        self.ant_button.setText('Роевой алгоритм')
        self.ant_button.setGeometry(MainWindow.window_width - 140, 90, 120, 30)
        self.ant_button.clicked.connect(self.calculate_ant_algorithm)

        self.ant_edit = QLineEdit(self)
        self.ant_edit.setGeometry(MainWindow.window_width - 140, 125, 100, 30)
        self.ant_edit.setEnabled(False)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.working_field)

    def mousePressEvent(self, event) -> None:
        mouse_coordinates = event.pos()
        if event.button() & Qt.LeftButton:
            if MainWindow.check_borders(mouse_coordinates) and MainWindow.check_collisions(mouse_coordinates):
                self.painter.setPen(Qt.blue)
                self.draw_point(mouse_coordinates.x(), mouse_coordinates.y(), point_number=Point.point_number)
                Point(mouse_coordinates.x(), mouse_coordinates.y())

                self.update()

    @staticmethod
    def check_borders(mouse_coordinates) -> bool:
        if mouse_coordinates.x() > 15:
            if mouse_coordinates.x() < MainWindow.window_width - 150 - 15:
                if mouse_coordinates.y() > 15:
                    if mouse_coordinates.y() < MainWindow.window_height - 15:
                        return True

    @staticmethod
    def check_collisions(mouse_coordinates) -> bool:
        if Point.points_dict != 0:
            for point in Point.points_dict.values():
                if math.sqrt((mouse_coordinates.x() - point.point_x) ** 2
                             + (mouse_coordinates.y() - point.point_y) ** 2) < 100:
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

    def calculate_greedy_algorithm(self) -> None:
        self.working_field.fill(Qt.white)
        total_way, order_list = functions.greedy(MainWindow.create_graph())
        self.painter.setPen(Qt.black)
        for i in range(len(order_list) - 1):
            self.draw_path(order_list[i], order_list[i + 1])
        for point_number, point in Point.points_dict.items():
            self.draw_point(point.point_x, point.point_y, point_number)
        self.update()
        self.greedy_edit.setText(str(total_way))

    def calculate_ant_algorithm(self) -> None:
        iterations = 10
        evaporation_coefficient = 0.2
        alpha, beta = 1, 1
        ant_route_generator = functions.ant_algorithm(MainWindow.create_graph(), iterations, alpha, beta,
                                                      evaporation_coefficient)
        for step in ant_route_generator:
            self.working_field.fill(Qt.white)
            for start_point, values in step.items():
                for i, destination_point in enumerate(values[0]):
                    self.painter.setPen(QPen(Qt.red, 45 * values[2][i]))
                    self.draw_path(start_point, destination_point)
            self.painter.setPen(Qt.black)
            for point_number, point in Point.points_dict.items():
                self.draw_point(point.point_x, point.point_y, point_number)
            sleep(0.1)
            self.update()

    def draw_point(self, x, y, point_number):
        self.painter.drawEllipse(x - 15, y - 15, 30, 30)
        if point_number < 10:
            self.painter.drawText(x - 3, y + 4, str(point_number))
        elif point_number < 100:
            self.painter.drawText(x - 6, y + 4, str(point_number))
        else:
            self.painter.drawText(x - 10, y + 4, str(point_number))

    def draw_path(self, start_point, end_point) -> None:
        start_x, start_y = Point.points_dict[start_point].point_x, Point.points_dict[start_point].point_y
        end_x, end_y = Point.points_dict[end_point].point_x, Point.points_dict[end_point].point_y
        self.painter.drawLine(start_x, start_y, end_x, end_y)


# class ThreadServerConnection(QThread):
#     def __init__(self, current_socket, label_server_status, plain_text_edit_status_report, connected_to_server_users):
#         QThread.__init__(self)
#         self.flag = True
#         self.server_socket = current_socket
#         self.label_server_status = label_server_status
#         self.plain_text_edit_status_report = plain_text_edit_status_report
#         self.connected_to_server_users = connected_to_server_users
#         self.thread_inputs_list = []
#
#     def run(self) -> None:
#         self.connection_update()
#
#     def connection_update(self):
#         while self.flag:
#             try:
#                 client, address = self.server_socket.accept()
#                 connected_user_name = client.recv(1024).decode('UTF-8')
#                 self.connected_to_server_users.append([client, address, connected_user_name])
#             except OSError:
#                 pass
#             else:
#                 current_time = strftime('%H:%M:%S', localtime())
#                 self.plain_text_edit_status_report.insertPlainText(f'{current_time} Connected {address} '
#                                                                    f'as @{connected_user_name}\n')
#                 thread_input = ThreadInput(self.connected_to_server_users[-1], 'server', self.connected_to_server_users,
#                                            None, self.label_server_status, self.plain_text_edit_status_report,
#                                            self.server_socket)
#                 self.thread_inputs_list.append(thread_input)
#                 thread_input.start()
#                 self.label_server_status.setText(f'Статус:\n'
#                                                  f'Сервер подключён\n'
#                                                  f'Количество подключённых пользователей: '
#                                                  f'{len(self.connected_to_server_users)}')
#                 if len(self.connected_to_server_users) > 1:
#                     for i in range(len(self.connected_to_server_users)):
#                         connected_to_server_users_string = ''
#                         for j, client in enumerate(self.connected_to_server_users):
#                             if j != i:
#                                 connected_to_server_users_string += f',{client[2]}'
#                         self.connected_to_server_users[i][0].send(f'USERS_LIST'
#                                                                   f'{connected_to_server_users_string}'.encode())
#
#     def stop(self):
#         for input_thread in self.thread_inputs_list:
#             input_thread.stop()
#         self.thread_inputs_list = []
#         for connection in self.connected_to_server_users:
#             connection[0].close()
#         self.flag = False

def optimal_path():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    optimal_path()
