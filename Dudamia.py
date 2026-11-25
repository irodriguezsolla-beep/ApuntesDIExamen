import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton


class GuiaGrid(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guía Visual QGridLayout")
        self.resize(500, 350)

        # 1. Creamos la rejilla (tabla de filas y columnas)
        grid = QGridLayout()

        # =====================================================================
        # FÓRMULA: grid.addWidget(boton, FILA, COLUMNA, ALTO, ANCHO)
        # =====================================================================

        # Celda normal (1x1) en Fila 0, Columna 0
        grid.addWidget(QPushButton("Normal (0, 0)"), 0, 0)

        # 2 DE LADO (ancho): Fila 0, Col 1 -> 1 de alto, 2 de ancho
        grid.addWidget(QPushButton("2 DE ANCHO (0, 1, 1, 2)"), 0, 1, 1, 2)

        # 2 DE ALTO (su celda + 1 abajo): Fila 1, Col 0 -> 2 de alto, 1 de ancho
        grid.addWidget(QPushButton("2 DE ALTO\n(1, 0, 2, 1)"), 1, 0, 2, 1)

        # Celdas normales en el medio (1x1)
        grid.addWidget(QPushButton("Normal (1, 1)"), 1, 1)
        grid.addWidget(QPushButton("Normal (1, 2)"), 1, 2)

        # Cuadrado grande 2x2: Fila 2, Col 1 -> 2 de alto, 2 de ancho
        grid.addWidget(QPushButton("GRANDE 2x2\n(2, 1, 2, 2)"), 2, 1, 2, 2)

        # Celda normal abajo a la izquierda (1x1)
        grid.addWidget(QPushButton("Normal (3, 0)"), 3, 0)

        # 2. Contenedor central obligatorio
        contenedor = QWidget()
        contenedor.setLayout(grid)
        self.setCentralWidget(contenedor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = GuiaGrid()
    ventana.show()
    sys.exit(app.exec())