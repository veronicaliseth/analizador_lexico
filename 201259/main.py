import ply.lex as lex
import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

qtCreatorFile = "View/main.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.analizar.clicked.connect(self.fn_iniciar)
        self.limpiar.clicked.connect(self.fn_limpiar)

    def fn_iniciar(self):
        datos = self.entrada.toPlainText()
        main(datos)
        
        self.table.setRowCount(len(resultado_lexema))
        self.table.setColumnCount(2)

        for i in range(len(resultado_lexema)):
            self.table.setItem(i, 0, QTableWidgetItem(tipo[i]))
            self.table.setItem(i, 1, QTableWidgetItem(simbolo[i]))

        self.reservadas.setText(f"Total de palabras reservadas:  {p_reservadas}")
        self.parentesis.setText(f"Total de parentesis:  {parentesis}")

        self.table.setHorizontalHeaderLabels(['Tipo', 'Simbolo'])

    def fn_limpiar(self):
        global p_reservadas, resultado_lexema
        global tipo, simbolo, parentesis
        tipo = []
        resultado_lexema = []
        simbolo = []
        parentesis = 0
        p_reservadas = 0

        self.entrada.clear()
        self.table.clearContents()
        self.table.setRowCount(0)
        self.reservadas.setText("Cantidad de palabras reservadas: ")
        self.parentesis.setText("Cantidad de Paréntesis: ")

resultado_lexema = []
tipo = []
simbolo = []
p_reservadas = 0
parentesis = 0

reservadas = ( 
    'FOR',
    'WHILE',
    'IF',
    'ELSE',
    'DO',
)

tokens = reservadas + (
    'LPAREN', # (
    'RPAREN', # )
    'ERROR'
)

t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_FOR(t):
    r'for'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_DO(t):
    r'do'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_EXCESS_RPAREN(t):
    r'\)\)+' # se detecta el exceso de parentesis derecho y solo permite un solo parentesis
    estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.type), str(t.value), str(t.lexpos))
    t.type = 'ERROR'
    tipo.append(t.type)
    simbolo.append(t.value)
    resultado_lexema.append(estado)  
    t.lexer.skip(1)
    print("Exceso de parentesis derecho")

def t_EXCESS_LPAREN(t):
    r'\(\(+' # se detecta el exceso de parentesis izquierdo y solo permite un solo parentesis
    print("Exceso de parentesis izquierdo")
    estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.type), str(t.value), str(t.lexpos))
    t.type = 'ERROR'
    tipo.append(t.type)
    simbolo.append(t.value)
    resultado_lexema.append(estado)  
    t.lexer.skip(1)

def t_ERROR(t):
    r'\w+(_\d\w)*'
    return t

def t_error(t):
    global resultado_lexema
    estado = "** Token no valido en la Linea {:4} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.value), str(t.lexpos))
    resultado_lexema.append(estado)
    tipo.append('TOKEN ILEGAL')
    simbolo.append(t.value[0])
    t.lexer.skip(1)

def main(entrada):
    global resultado_lexema
    global tipo, simbolo, p_reservadas, parentesis

    analizador = lex.lex()
    analizador.input(entrada)

    while True:
        tok = analizador.token()
        if not tok:
            break
        estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno), str(tok.type), str(tok.value), str(tok.lexpos))
        resultado_lexema.append(estado)
        if tok.type == 'LPAREN' or tok.type == 'RPAREN':
            parentesis = parentesis + 1
        if tok.type in reservadas:
            p_reservadas = p_reservadas + 1
            dato_tipo = 'RESERVADA' + ' ' + str(tok.type)
            tipo.append(dato_tipo)
        else:
            tipo.append(tok.type)
        simbolo.append(tok.value)
    for i in resultado_lexema:
        print(i)

analizador = lex.lex()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())