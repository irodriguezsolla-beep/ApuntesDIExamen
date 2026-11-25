from PyQt6.QtCore import Qt, QAbstractListModel
from PyQt6.QtGui import QImage, QColor
from PyQt6.QtWidgets import QMainWindow

# Carga una imagen de un tic verde (aunque luego está comentada abajo)
tick = QImage("tick.png").scaled(16, 16)


# Heredamos de QAbstractListModel para crear nuestro modelo de lista personalizado
class ModeloTarefas(QAbstractListModel):
    def __init__(self, tarefas=None):
        super().__init__()
        # Guarda la lista que le pasemos (ej: [[True, "Ir al gimnasio"], ...])
        # Si no le pasamos nada, crea una lista vacía []
        self.tarefas = tarefas or []

    # 1. PREGUNTA DEL QLISTVIEW: "¿Qué tengo que dibujar en esta fila?"
    # 'indice' nos dice qué fila es (indice.row())
    # 'rol' nos dice QUÉ cosa quiere dibujar (el texto, el checkbox, el color...)
    def data(self, indice, rol):

        # Si pide el TEXTO normal (DisplayRole):
        if rol == Qt.ItemDataRole.DisplayRole:
            # Desempaqueta la pareja [estado, texto]. La barra baja (_) ignora el estado
            _, texto = self.tarefas[indice.row()]
            return texto  # Devuelve solo el texto para pintarlo en pantalla

        """ (Código comentado del profesor por si quisiera poner iconos o fondo verde)
        if rol == Qt.ItemDataRole.DecorationRole:
            estado,_ = self.tarefas[indice.row()]
            if estado:
                return tick

        if rol == Qt.ItemDataRole.BackgroundRole:
            estado,_ = self.tarefas[indice.row()]
            if estado:
                return QColor("lightgreen")
        """

        # Si pide el ESTADO DEL CHECKBOX (CheckStateRole):
        if rol == Qt.ItemDataRole.CheckStateRole:
            # Saca el True/False de esa fila e ignora el texto (_)
            estado, _ = self.tarefas[indice.row()]
            # Convierte True/False en un checkbox marcado o desmarcado de Qt
            return Qt.CheckState(estado)

    # 2. ACCIÓN DEL USUARIO: "El usuario ha hecho clic en un checkbox o editado un texto"
    # 'valor' es el nuevo estado (marcado/desmarcado) o el nuevo texto
    def setData(self, indice, valor, rol):
        # Si el usuario tocó el checkbox (CheckStateRole):
        if rol == Qt.ItemDataRole.CheckStateRole:
            # Actualiza el primer elemento [0] (True/False) de esa fila en nuestra lista
            self.tarefas[indice.row()][0] = valor
            # Avisa a la pantalla de que los datos cambiaron para que se vuelva a dibujar
            self.layoutChanged.emit()
            return True  # Confirma que el cambio se guardó bien

        # Si el usuario editó el texto (EditRole):
        if rol == Qt.ItemDataRole.EditRole:
            # Actualiza el segundo elemento [1] (el texto) de esa fila
            self.tarefas[indice.row()][1] = valor
            self.layoutChanged.emit()
            return True

        return False

    # 3. PREGUNTA DEL QLISTVIEW: "¿Cuántas filas tiene la lista en total?"
    def rowCount(self, indice):
        return len(self.tarefas)  # Devuelve el tamaño de la lista de Python

    # 4. PREGUNTA DEL QLISTVIEW: "¿Qué permisos tiene cada fila?"
    def flags(self, indice):
        # Combinamos 3 permisos con la barra vertical (|):
        # - ItemIsUserCheckable: El usuario puede marcar/desmarcar la casilla
        # - ItemIsEnabled: La fila está activa (no sale en gris)
        # - ItemIsSelectable: El usuario puede hacer clic para seleccionar la fila (se pone azul)
        return Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable