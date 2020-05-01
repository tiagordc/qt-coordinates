import sys, math, pyperclip
from PyQt5 import QtWidgets, QtGui, QtCore
from pynput.mouse import Listener, Controller

def get_pos(x, y):
    try:
        geo = app.screenAt(QtCore.QPoint(x, y)).geometry()
        pos_x = x - geo.left()
        pos_y = y - geo.top()
        perct_x = "{:.4f}".format(pos_x / geo.width()) 
        perct_y = "{:.4f}".format(pos_y / geo.height())
        return perct_x, perct_y
    except: 
        return 0, 0

class Coordinates(QtWidgets.QLabel):

    def __init__(self, position):
        super().__init__(None)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("font-size: 10px")
        self.setPosition(position[0], position[1])
        self.setAlignment(QtCore.Qt.AlignCenter)
    
    def setPosition(self, x, y):
        pos = get_pos(x, y)
        self.setText(str(pos))
        x = x if float(pos[0]) < 0.5 else x - 99
        y = y if float(pos[1]) < 0.5 else y - 19
        self.setGeometry(x, y, 100, 20)


app = QtWidgets.QApplication(sys.argv)

def on_click(x, y, button, pressed):
    if not pressed: # released
        global last
        elapsed = QtCore.QDateTime.currentMSecsSinceEpoch() - last
        last = QtCore.QDateTime.currentMSecsSinceEpoch()
        pos = str(get_pos(x, y))
        pyperclip.copy(pos)
        print(pos)
        if elapsed < 250: # quit on double click
            app.quit()
            return False

def on_move(x, y):
    win.setPosition(x, y)

listener = Listener(on_click=on_click, on_move=on_move)
listener.start()
last = QtCore.QDateTime.currentMSecsSinceEpoch()

mouse = Controller()
win = Coordinates(mouse.position)
win.show()

sys.exit(app.exec())
