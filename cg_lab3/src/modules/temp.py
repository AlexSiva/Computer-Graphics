from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QBrush, QFont
import sys

class GridItem(QGraphicsItem):
    def __init__(self, size, spacing):
        super(GridItem, self).__init__()

        self.size = size
        self.spacing = spacing
        self.cell_size = 20
        self.cells = []

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        pen = painter.pen()
        pen.setColor(Qt.lightGray)
        painter.setPen(pen)

        # Рисование вертикальных линий
        for i in range(0, self.size, self.spacing):
            painter.drawLine(i, 0, i, self.size)

        # Рисование горизонтальных линий
        for i in range(0, self.size, self.spacing):
            painter.drawLine(0, i, self.size, i)

        # Закрашивание клеток
        brush = QBrush(Qt.gray, Qt.SolidPattern)
        painter.setBrush(brush)

        for cell in self.cells:
            painter.drawRect(cell)

class CoordinateSystemItem(QGraphicsItem):
    def __init__(self, size):
        super(CoordinateSystemItem, self).__init__()

        self.size = size

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        pen = painter.pen()
        pen.setColor(Qt.black)
        painter.setPen(pen)

        # Рисование осей
        painter.drawLine(0, self.size / 2, self.size, self.size / 2)
        painter.drawLine(self.size / 2, 0, self.size / 2, self.size)

        # Добавление подписей к осям
        font = QFont()
        font.setPixelSize(12)
        painter.setFont(font)

        painter.drawText(self.size / 2 + 5, 15, "Y")
        painter.drawText(self.size - 15, self.size / 2 - 5, "X")

class MyCanvas(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создание QGraphicsScene и QGraphicsView
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene)

        # Создание элементов сетки и системы координат
        grid_item = GridItem(500, 20)
        coordinate_system_item = CoordinateSystemItem(500)

        scene.addItem(grid_item)
        scene.addItem(coordinate_system_item)

        # Обработка событий колеса мыши для масштабирования
        view.setRenderHint(QPainter.Antialiasing)
        view.setMouseTracking(True)
        view.viewport().setMouseTracking(True)
        view.setRenderHint(QPainter.Antialiasing, True)

        def wheel_event(event):
            factor = 1.2
            if event.angleDelta().y() < 0:
                factor = 1.0 / factor
            view.scale(factor, factor)

        view.wheelEvent = wheel_event

        # Обработка событий клика мыши для закрашивания клеток
        def mousePressEvent(event):
            pos = view.mapToScene(event.pos())
            grid_item.add_cell(pos.x() // grid_item.spacing * grid_item.spacing,
                               pos.y() // grid_item.spacing * grid_item.spacing)

        view.mousePressEvent = mousePressEvent

        # Установка QGraphicsView как центрального виджета главного окна
        self.setCentralWidget(view)

        # Установка размеров главного окна
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Сетка с масштабированием, закрашиванием и системой координат в PyQt')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyCanvas()
    window.show()
    sys.exit(app.exec_())
