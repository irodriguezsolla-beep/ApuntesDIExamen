import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from modeloTabla import ModeloTabla


class FiestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tabla con Añadir")
        self.setMinimumSize(600, 350)
        self.setMaximumSize(1000, 1000)

        # Organizador principal (de arriba a abajo)
        caixaV = QVBoxLayout()

        # 1. DATOS INICIALES DE LA TABLA
        self.datos = [
            ["Nome", "DNI", "Xenero", "Falecimento"],
            ["Ana Perez", "1111R", "Muller", False],
            ["Paco Porras", "2222T", "Home", True],
            ["Roque Vila", "3333H", "Home", False]
        ]

        # 2. TABLA Y MODELO
        self.modelo = ModeloTabla(self.datos)
        self.tvwTaboa = QTableView()
        self.tvwTaboa.setModel(self.modelo)
        caixaV.addWidget(self.tvwTaboa)

        # =====================================================================
        # 3. FORMULARIO DEBAJO DE LA TABLA PARA AÑADIR FILAS NUEVAS
        # =====================================================================
        caixa_engadir = QHBoxLayout()  # Organizador horizontal (izquierda a derecha)

        # Recuadro de texto para el Nombre
        self.txt_nome = QLineEdit()
        self.txt_nome.setPlaceholderText("Nome")  # Texto gris orientativo dentro de la caja
        caixa_engadir.addWidget(self.txt_nome)

        # Recuadro de texto para el DNI
        self.txt_dni = QLineEdit()
        self.txt_dni.setPlaceholderText("DNI")
        caixa_engadir.addWidget(self.txt_dni)

        # Lista desplegable para el Género ("Home" / "Muller")
        self.cmb_xenero = QComboBox()
        self.cmb_xenero.addItems(["Home", "Muller"])
        caixa_engadir.addWidget(self.cmb_xenero)

        # Checkbox para Vivo (desmarcado = False) o Muerto (marcado = True)
        self.chk_falecido = QCheckBox("Falecido")
        caixa_engadir.addWidget(self.chk_falecido)

        # Botón Añadir
        self.btn_engadir = QPushButton("Añadir")
        self.btn_engadir.clicked.connect(self.engadir_fila)  # Conecta el clic con la función
        caixa_engadir.addWidget(self.btn_engadir)

        # Metemos toda esta fila de controles debajo de la tabla
        caixaV.addLayout(caixa_engadir)

        # 4. CONTENEDOR CENTRAL OBLIGATORIO
        contenedor = QWidget()
        contenedor.setLayout(caixaV)
        self.setCentralWidget(contenedor)

        self.show()

    # =========================================================================
    # FUNCIÓN QUE SE EJECUTA AL PULSAR "AÑADIR"
    # =========================================================================
    def engadir_fila(self):
        # 1. Recogemos lo que hay escrito/seleccionado en los controles de abajo
        nome = self.txt_nome.text()
        dni = self.txt_dni.text()
        xenero = self.cmb_xenero.currentText()          # Lee "Home" o "Muller"
        falecido = self.chk_falecido.isChecked()        # Devuelve True si está marcado, False si no

        # Solo añade la fila si el usuario escribió al menos nombre y DNI
        if nome != "" and dni != "":
            # 2. Añadimos la nueva fila a la lista de datos de Python
            self.datos.append([nome, dni, xenero, falecido])

            # 3. OBLIGATORIO: Avisamos al modelo de que hay una fila nueva para que la dibuje
            self.modelo.layoutChanged.emit()

            # 4. Limpiamos los campos de abajo para dejarlos listos para el siguiente
            self.txt_nome.clear()
            self.txt_dni.clear()
            self.cmb_xenero.setCurrentIndex(0)
            self.chk_falecido.setChecked(False)


if __name__ == '__main__':
    aplicacion = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    aplicacion.exec()