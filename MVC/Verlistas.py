import sys
import math

from PyQt6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit,
                             QHBoxLayout, QListView)
from PyQt6.QtGui import QColor, QPalette

# Importamos la clase del archivo anterior
from ModeloTarefa import ModeloTarefas


class FiestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("exemplo QListView")
        self.setMinimumSize(400, 600)
        self.setMaximumSize(400, 400)

        # 1. DATOS INICIALES: Lista de listas. Cada elemento es [está_hecha, "Nombre tarea"]
        self.listaTarefas = [
            [True, "Ir o centro DC"],
            [False, "Ir o ximnasio"],
            [False, "Ir a compra"],
            [False, "Outra"]
        ]

        # 2. CREAMOS EL MODELO pasándole nuestra lista de datos
        self.modelo = ModeloTarefas(self.listaTarefas)

        # Organizador principal vertical (de arriba a abajo)
        caixaV = QVBoxLayout()

        # 3. CREAMOS LA VISTA (QListView) y le enchufamos el modelo
        self.lstTarefas = QListView()
        self.lstTarefas.setModel(self.modelo)  # Conecta los ojos con el cerebro
        # Permite seleccionar varias tareas a la vez haciendo clic en ellas (MultiSelection)
        self.lstTarefas.setSelectionMode(QListView.SelectionMode.MultiSelection)
        caixaV.addWidget(self.lstTarefas)

        # 4. BOTONES HORIZONTALES
        caixaBotons = QHBoxLayout()

        btnBorrar = QPushButton("Borrar")
        btnBorrar.clicked.connect(self.on_btnBorrar_clicked)  # Conecta clic -> borrar

        btnFeito = QPushButton("Feito")
        btnFeito.clicked.connect(self.on_btnFeito_clicked)    # Conecta clic -> marcar hecho

        caixaBotons.addWidget(btnBorrar)
        caixaBotons.addWidget(btnFeito)

        caixaV.addLayout(caixaBotons)

        # 5. CAJA DE TEXTO Y BOTÓN PARA AÑADIR TAREA NUEVA
        self.txtTarefa = QLineEdit()  # Caja donde escribes la nueva tarea
        caixaV.addWidget(self.txtTarefa)

        btnEngadir = QPushButton("Engadir Tarefa")
        btnEngadir.clicked.connect(self.on_btnEngadir_clicked)  # Conecta clic -> añadir
        caixaBotons.addWidget(btnEngadir)

        # Contenedor central obligatorio en QMainWindow
        contenedor = QWidget()
        contenedor.setLayout(caixaV)
        self.setCentralWidget(contenedor)

        self.show()

    # =========================================================================
    # FUNCIONES DE LOS BOTONES
    # =========================================================================

    # Botón BORRAR: Elimina las tareas que estén seleccionadas en azul
    def on_btnBorrar_clicked(self):
        # Pide a la vista la lista de filas seleccionadas
        pos = self.lstTarefas.selectedIndexes()
        for indice in pos:
            # Elimina esa posición de la lista de Python
            self.listaTarefas.pop(indice.row())
        # OBLIGATORIO: Avisa al modelo de que la lista cambió para refrescar la pantalla
        self.modelo.layoutChanged.emit()
        # Quita la selección azul de la lista
        self.lstTarefas.clearSelection()

    # Botón FEITO: Marca como True (hechas) las tareas seleccionadas en azul
    def on_btnFeito_clicked(self):
        indices = self.lstTarefas.selectedIndexes()

        for indice in indices:
            # Saca el texto actual de esa fila (ignorando el estado viejo con _)
            _, texto = self.listaTarefas[indice.row()]
            # Sobrescribe esa fila poniendo True (hecha) y manteniendo su texto
            self.listaTarefas[indice.row()] = (True, texto)

        # Refresca la pantalla y limpia la selección azul
        self.modelo.layoutChanged.emit()
        self.lstTarefas.clearSelection()

    # Botón ENGADIR TAREFA: Añade lo escrito en el QLineEdit a la lista
    def on_btnEngadir_clicked(self):
        txt = self.txtTarefa.text()  # Lee lo que escribió el usuario

        # Solo añade si la caja no está vacía
        if txt != "":
            # Añade una nueva pareja [False (sin hacer), texto] al final de la lista
            self.listaTarefas.append([False, self.txtTarefa.text()])
            self.txtTarefa.clear()  # Vacía la caja de texto
            self.modelo.layoutChanged.emit()  # Refresca la lista en pantalla


# Arranque de la aplicación
if __name__ == '__main__':
    aplicacion = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    aplicacion.exec()