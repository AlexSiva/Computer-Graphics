from PyQt5.QtWidgets import QMainWindow, QGraphicsLineItem, QLineEdit, QPushButton, QLabel, QRadioButton, QButtonGroup, QGridLayout, QToolTip, QWidget, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QBrush, QPen
from modules.grid import GridItem
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 0 - Пошаговый     1 - Брезенхема
        self.state = 0
        self.line_item = None

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout()
        
        self.setup_canvas()
        self.setup_radio_buttons()
        self.setup_line_chooser()
        self.setup_time_label()

        central_widget.setLayout(self.layout)

    def setup_line_chooser(self):
        x0_label = QLabel('X0:')
        y0_label = QLabel('Y0:')
        x1_label = QLabel('X1:')
        y1_label = QLabel('Y1:')

        self.x0_edit = QLineEdit()
        self.y0_edit = QLineEdit()
        self.x1_edit = QLineEdit()
        self.y1_edit = QLineEdit()

        self.ok_button = QPushButton('Draw line')
        self.ok_button.clicked.connect(self.ok_button_toggled)

        self.layout.addWidget(x0_label, 1, 1)
        self.layout.addWidget(y0_label, 2, 1)
        self.layout.addWidget(x1_label, 1, 3)
        self.layout.addWidget(y1_label, 2, 3)

        self.layout.addWidget(self.x0_edit, 1, 2)
        self.layout.addWidget(self.y0_edit, 2, 2)
        self.layout.addWidget(self.x1_edit, 1, 4)
        self.layout.addWidget(self.y1_edit, 2, 4)

        self.layout.addWidget(self.ok_button, 1, 5, 2, 1)
    
    def convert_x_cord(self, x):
        return x * self.grid_spacing

    def convert_y_cord(self, y):
        return y * self.grid_spacing 
    
    def convert_x_cord_center(self, x):
        return x * self.grid_spacing + self.grid_spacing // 2

    def convert_y_cord_center(self, y):
        return y * self.grid_spacing + self.grid_spacing // 2

    def draw_line(self, x0, y0, x1, y1):
        if self.line_item in self.scene.items():
            self.scene.removeItem(self.line_item)
        
        self.line_item = QGraphicsLineItem(self.convert_x_cord_center(x0), self.convert_y_cord_center(y0), self.convert_x_cord_center(x1), self.convert_y_cord_center(y1))
        pen = QPen(Qt.red)
        self.line_item.setPen(pen)
        self.scene.addItem(self.line_item)

    def ok_button_toggled(self):
        self.grid_item.clear_cells()
        self.grid_item.clear_pixels()
        x0 = self.x0_edit.text()
        y0 = self.y0_edit.text()
        x1 = self.x1_edit.text()
        y1 = self.y1_edit.text()
        try:
            x0 = int(x0)
            y0 = int(y0)
            x1 = int(x1)
            y1 = int(y1)

            self.draw_line(x0, y0, x1, y1)
            
            start_time = time.perf_counter()
            if self.state == 0:
                self.step_algorithm(x0, y0, x1, y1)
            elif self.state == 1:
                self.brezenhem_algorithm(x0, y0, x1, y1)
            end_time = time.perf_counter()

            delta_time = (end_time - start_time) * 1e6
            delta_time = round(delta_time, 2)
            self.time_label.setText('Time: ' + str(delta_time) + ' microseconds')

        except ValueError:
            print('Convert error!')
        except Exception as ignored:
            print(ignored)

    def step_algorithm(self, x0, y0, x1, y1):
        x = x0
        y = y0

        k = (y1 - y0) / (x1 - x0)
        b = y1 - k * x1
        steps = max(abs(x1 - x0), abs(y1 - y0))

        sign = 0
        if x1 - x0 > 0:
            sign = 1
        else:
            sign = -1
        step = sign * abs(x1 - x0) / steps

        for i in range(steps + 1):
            self.brush_cell(x, y)
            x += step
            y = round(k * x + b)

    def setup_time_label(self):
        self.time_label = QLabel('Time: ')
        self.layout.addWidget(self.time_label, 3, 0)

    def brezenhem_algorithm(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            # Рисуем текущий пиксель
            self.brush_cell(x0, y0)

            # Проверяем, достигли ли конечной точки
            if x0 == x1 and y0 == y1:
                break

            # Вычисляем ошибку и корректируем координаты
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    
    def brush_cell(self, x, y):
        x = self.convert_x_cord_center(x)
        y = self.convert_y_cord_center(y)
        self.grid_item.add_cell(x // self.grid_item.spacing * self.grid_item.spacing,
                               y // self.grid_item.spacing * self.grid_item.spacing)
    
    def draw_point(self, x, y):
        x = self.convert_x_cord(x)
        y = self.convert_y_cord(y)
        self.grid_item.add_pixel(round(x), round(y))

    def setup_radio_buttons(self):
        self.step_radio_button = QRadioButton('Пошаговый алгортим')
        self.step_radio_button.setChecked(True)
        self.brezenhem_radio_button = QRadioButton('Алгоритм Брезенхема')
        
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.step_radio_button)
        self.button_group.addButton(self.brezenhem_radio_button)

        self.step_radio_button.toggled.connect(self.step_button_toggled)
        self.brezenhem_radio_button.toggled.connect(self.brezenhem_button_toggled)

        self.layout.addWidget(self.step_radio_button, 1, 0)
        self.layout.addWidget(self.brezenhem_radio_button, 2, 0)

    def step_button_toggled(self):
        self.state = 0
    
    def brezenhem_button_toggled(self):
        self.state = 1


    def setup_canvas(self):
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        self.grid_size = 2500
        self.grid_spacing = 25

        self.grid_item = GridItem(self.grid_size, self.grid_spacing)
        self.scene.addItem(self.grid_item)

        # Обработка событий колеса мыши для масштабирования
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMouseTracking(True)
        self.view.viewport().setMouseTracking(True)
        self.view.setRenderHint(QPainter.Antialiasing, True)
        self.view.scale(0.65, 0.65)

        def wheel_event(event):
            factor = 1.2
            if event.angleDelta().y() < 0:
                factor = 1.0 / factor
            self.view.scale(factor, factor)

        self.view.wheelEvent = wheel_event

        def mouseMoveEvent(event):
            # Получаем координаты мыши в системе координат QGraphicsView
            pos = event.pos()
            scene_pos = self.view.mapToScene(pos)

            # Форматируем координаты для отображения в QToolTip
            tooltip_text = f"X: {int(scene_pos.x() // self.grid_spacing)}, Y: {int(scene_pos.y() // self.grid_spacing)}"

            # Устанавливаем текст в QToolTip
            pos = self.mapToGlobal(pos)
            QToolTip.showText(pos, tooltip_text, self)

        self.view.mouseMoveEvent = mouseMoveEvent

        self.layout.addWidget(self.view, 0, 0, 1, 6)

    