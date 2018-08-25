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
        self.setGeometry(300, 500, 300, 150) # window geometry

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

    '''
    1) SetInputValue 메서드를 사용해 TR 입력 값을 설정합니다. 
    2) CommRqData 메서드를 사용해 TR을 서버로 송신합니다. 
    3) 서버로부터 이벤트가 발생할 때까지 이벤트 루프를 사용해 대기합니다. 
    4) CommGetData 메서드를 사용해 수신 데이터를 가져옵니다. 
    '''

    # btn1 event 처리 과정
    def btn1_clicked(self): # btn1 event 발생 시 처리하는 과정
        code = self.code_edit.text() # code_edit에 입력되는 값을 불러와서 code로 정의
        self.text_edit.append("종목코드: " + code) # text edit section에 종목코드:
        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        self.text_edit.append("계좌번호: " + account_num.rstrip(';'))

        # SetInputValue : TR input value를 설정
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code) # SetInputValue를 파이썬에서 사용할 수 있도록 호출

        # CommRqData # CommRqData 메서드를 사용해 TR을 서버로 송신
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101") # CommRqData를 파이썬에서 사용할 수 있도록 호출

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10001_req":
            # ComGetData 메서드를 사용해 수신데이터를 가져온다.
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            # name이라는 변수는 CommGetData 메서드를 통해 trcode, rqname을 송신받음.
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")
            # volume이라는 변수는 CommGetData 메서드를 통해 trcode, rqname을 송신받음.


            self.text_edit.append("종목명: " + name.strip()) # text_edit에 종목명: name.strip()을 출력
            # self.strip()은 좌우 공백을 모두 자르는 method
            self.text_edit.append("거래량: " + volume.strip()) # text_edit에 거래량: volume.strip()을 출력

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow() # myWindow class를 MyWindow() 생성자 클래스로 정의
    myWindow.show() # myWindow를 개별 화면으로 출력
    app.exec_()