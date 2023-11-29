from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QFont
import sys


class GridItem(QGraphicsItem):
    def __init__(self, size, spacing):
        super(GridItem, self).__init__()

        self.size = size
        self.spacing = spacing
        self.cell_size = spacing
        self.cells = []

        self.pixels = []

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        pen = painter.pen()
        pen.setColor(Qt.lightGray)
        painter.setPen(pen)
        pen_axis = painter.pen()
        pen_axis.setColor(Qt.black)

        # Рисование вертикальных линий
        for i in range(0, self.size, self.spacing):
            painter.drawLine(i, 0, i, self.size)

        # Рисование горизонтальных линий
        for i in range(0, self.size, self.spacing):
            painter.drawLine(0, i, self.size, i)

        half_size = int(self.size / 2)

        painter.setPen(pen_axis)
        painter.drawLine(0, 0, 0, self.size)
        painter.drawLine(0, 0, self.size, 0)
        number_size = self.spacing // 5
        painter.setFont(QFont('Arial', number_size))

        x_delta = self.spacing // 4
        y_delta = self.spacing // 2
        # Рисование горизонтальных подписей
        for i in range(0, self.size, self.spacing):
            temp = i // self.spacing
            painter.drawText(QPoint(i + x_delta, y_delta), str(temp))
            painter.drawLine(0, i, 3, i)

        # Рисование вертикальных подписей
        for i in range(0, self.size, self.spacing):
            temp = i // self.spacing
            if(temp > 0):
                painter.drawText(QPoint(x_delta, i + 2 + y_delta), str(temp))
            painter.drawLine(i, 0, i, 3)

        painter.setFont(QFont('Arial', 12))
        painter.drawText(QPoint(self.size, 30), 'X')
        painter.drawText(QPoint(-30, self.size), 'Y')

        painter.setPen(pen)

        # Закрашивание клеток
        brush = QBrush(Qt.gray, Qt.SolidPattern)
        painter.setBrush(brush)

        for cell in self.cells:
            painter.drawRect(cell)
        
        pen_dot = painter.pen()
        pen_dot.setColor(Qt.blue)
        painter.setPen(pen_dot)
        brush = QBrush(Qt.blue, Qt.SolidPattern)
        painter.setBrush(brush)
        for point in self.pixels:
            painter.drawEllipse(point)

    def add_cell(self, x, y):
        cell_rect = QRectF(x, y, self.cell_size, self.cell_size)
        self.cells.append(cell_rect)
        self.update()

    def clear_cells(self):
        self.cells = []
        self.update()

    def add_pixel(self, x, y):
        point = QRectF(x - 2, y - 2, 2 * 2, 2 * 2)
        self.pixels.append(point)
        self.update()
    
    def clear_pixels(self):
        self.pixels = []
        self.update()