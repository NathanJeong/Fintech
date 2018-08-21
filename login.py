import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Kiwoom Login
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1") # QAxWidget
        self.kiwoom.dynamicCall("CommConnect()") # ComConnect method를 파이썬에서 사용할 수 있도록 함

        # OpenAPI+ Event
        self.kiwoom.OnEventConnect.connect(self.event_connect) # 통신 연결 상태 변경시 이벤트
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata) # Tran 수신시 이벤트

        self.setWindowTitle("PyStock") # window title
        self.setGeometry(300, 300, 300, 150) # window geometry

        label = QLabel('종목코드: ', self) # label name
        label.move(20, 20) # label location

        self.code_edit = QLineEdit(self) # input section
        self.code_edit.move(70, 20) # input location (x,y)
        self.code_edit.setText("") # default value

        btn1 = QPushButton("조회", self) # button widget
        btn1.move(190, 20) # button widget location (x,y)
        btn1.clicked.connect(self.btn1_clicked) # 클릭 event를 처리해주는 과정을 연결

        self.text_edit = QTextEdit(self) #
        self.text_edit.setGeometry(10, 60, 280, 80) # text output location(x,y,width, height)
        self.text_edit.setEnabled(False) #

    def event_connect(self, err_code): # event_connect event 발생 시 처리하는 과정
        if err_code == 0: # OnEventConnect method는 로그인 성공시 0을 반환
            self.text_edit.append("로그인 성공")
        else:
            self.text_edit.append("로그인 실패, 아이디 혹은 비밀번호가 틀렸습니다.")

    def btn1_clicked(self): # btn1 event 발생 시 처리하는 과정
        code = self.code_edit.text() # code_edit에 입력되는 값을 불러와서 code로 정의
        self.text_edit.append("종목코드: " + code) # text edit section에 종목코드:

        # SetInputValue : TR input value를 설정
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code) # SetInputValue를 파이썬에서 사용할 수 있도록 호출

        # CommRqData # CommRqData 메서드를 사용해 TR을 서버로 송신
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101") # CommRqData를 파이썬에서 사용할 수 있도록 호출

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10001_req":
            # ComGetData 메서드를 사용해 수신데이터를 가져온다.
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")

            self.text_edit.append("종목명: " + name.strip())
            self.text_edit.append("거래량: " + volume.strip())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()