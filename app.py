import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from main_window import MainWindow
from database import Database
import config

def main():
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
