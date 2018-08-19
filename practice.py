import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# app = QApplication(sys.argv)
# print(sys.argv) # absolute location of present source code
# label1 = QLabel("Hello PyQt") # label
# label2 = QPushButton("Quit") # button
# label1.show()
# label2.show()
# app.exec_()

class MyWindow(QMainWindow): # QMainWindow의 메서드를 모두 상속
    def __init__(self): # 생성자
        super().__init__() # 부모 클래스에 정의된 __init__()를 호출 (생성자)
        self.setWindowTitle("PyStock") # Title
        self.setGeometry(300, 300, 300, 400) # Window geometry

        btn1 = QPushButton("Click me", self) # add button and its contents
        btn1.move(20,20) # output location of btn1 in Window geometry
        btn1.clicked.connect(self.btn1_clicked) # connect btn1 and btn_clicked function

    def btn1_clicked(self): # output message when button was clicked
        QMessageBox.about(self, "message", "clicked") # message = window title, clicked = contents


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()