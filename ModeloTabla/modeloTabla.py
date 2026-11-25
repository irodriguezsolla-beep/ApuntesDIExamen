from PyQt6.QtCore import Qt, QAbstractTableModel


class ModeloTabla(QAbstractTableModel):
    def __init__(self, taboa):
        super().__init__()
        self.taboa = taboa

    def rowCount(self, indice):
        return len(self.taboa)

    def columnCount(self, indice):
        return len(self.taboa[0])

    def data(self, indice, rol):
        if indice.isValid():
            fila = indice.row()
            col = indice.column()

            # 1. TEXTO EN LA CELDA (DisplayRole)
            if rol == Qt.ItemDataRole.DisplayRole:
                # Si es la columna 3 y NO es la cabecera (fila != 0),
                # devuelve "True" o "False" como texto al lado del checkbox
                if fila != 0 and col == 3:
                    return str(self.taboa[fila][col])
                # Para el resto de celdas (incluyendo la cabecera), devuelve su texto normal
                return str(self.taboa[fila][col])

            # 2. CHECKBOX EN LA CELDA (CheckStateRole)
            if rol == Qt.ItemDataRole.CheckStateRole:
                # En la columna 3 (a partir de la fila 1) dibuja el cuadradito marcado o desmarcado
                if fila != 0 and col == 3:
                    return Qt.CheckState.Checked if self.taboa[fila][col] else Qt.CheckState.Unchecked

    def setData(self, indice, valor, rol):
        fila = indice.row()
        col = indice.column()

        # Cuando el usuario hace clic en el checkbox de la tabla (columna 3)
        if rol == Qt.ItemDataRole.CheckStateRole and fila != 0 and col == 3:
            # Guarda True si se marcó, o False si se desmarcó
            self.taboa[fila][col] = (valor == Qt.CheckState.Checked.value)
            # Refresca la tabla para que el texto cambie entre "True" y "False" al instante
            self.layoutChanged.emit()
            return True

        # Cuando el usuario edita un texto haciendo doble clic (columnas 0 y 2)
        if rol == Qt.ItemDataRole.EditRole and fila != 0 and col != 1 and col != 3:
            self.taboa[fila][col] = valor
            self.layoutChanged.emit()
            return True

        return False

    def flags(self, indice):
        condicion = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        if indice.row() != 0:  # La fila 0 (títulos) no se toca
            if indice.column() == 3:
                # La columna 3 tiene checkbox clicable
                condicion = condicion | Qt.ItemFlag.ItemIsUserCheckable
            elif indice.column() != 1:
                # Las columnas 0 y 2 se pueden editar con doble clic (el DNI no)
                condicion = condicion | Qt.ItemFlag.ItemIsEditable

        return condicion