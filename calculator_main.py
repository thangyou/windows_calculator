import sys
import math
import numpy as np # atom numpy 설치 방법 확인 -> 실행 확인? ✓
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class QPushButtonOperation(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        font = QFont("Helvetia", 13)
        font.setBold(True)
        self.setFont(font)

class QPushButtonNumber(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        font = QFont("Helvetia", 13)
        font.setBold(True)
        self.setFont(font)

class QPushButtonEqual(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        font = QFont("Helvetia", 13)
        font.setBold(True)
        self.setFont(font)

class QLineEdit(QLineEdit):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignRight)
        font = QFont("Helvetia", 13)
        self.setFont(font)

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "계산기"
        self.setWindowTitle(self.title)
        self.setGeometry(700, 350, 400, 400)
        self.set_style()
        self.init_ui()

    def set_style(self):
        with open("style_btn.css", 'r') as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        ### 레이아웃 설정
        main_layout = QGridLayout()
        layout_equation_solution = QGridLayout()
        layout_operation1 = QGridLayout() # 추가 연산
        layout_operation2 = QGridLayout() # 기본 연산
        layout_number = QGridLayout()

        ### global var
        self.temp_number = 0 # 기본 연산 결과
        self.temp_another = 0 # 추가 연산 결과
        self.temp_operator = ""
        self.fin_calc = 0 # 계산 완료 상태 변수 (False)

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 통합 - issue #10
        layout_equation_solution = QGridLayout()
        self.equation = QLineEdit("")
        layout_equation_solution.addWidget(self.equation)

        ### 연산 버튼
        button_plus = QPushButtonOperation("+")
        button_minus = QPushButtonOperation("-")
        button_product = QPushButtonOperation("x")
        button_equal = QPushButtonEqual("=")

        ### 연산 버튼을 클릭했을 때, 각 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_equal.clicked.connect(self.button_equal_clicked)

        ### 버튼을 layout_operation2 레이아웃에 추가
        layout_operation2.addWidget(button_product, 0, 0)
        layout_operation2.addWidget(button_minus, 1, 0)
        layout_operation2.addWidget(button_plus, 2, 0)
        layout_operation2.addWidget(button_equal, 3, 0)

        ### 기존 계산기에 없는 항목(버튼)들 추가
        button_rest = QPushButtonOperation("%")
        button_clear = QPushButtonOperation("C") # Clear All
        button_c_entry = QPushButtonOperation("CE") # Clear last char
        button_backspace = QPushButtonOperation("<")

        button_inverse = QPushButtonOperation("1/x") # 역수
        button_square = QPushButtonOperation("x²") # 제곱
        button_squ_root = QPushButtonOperation("²√x") # 제곱근
        button_division = QPushButtonOperation("/")

        ### 버튼 클릭 시 시그널 설정
        button_rest.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_clear.clicked.connect(self.button_clear_clicked)
        button_c_entry.clicked.connect(self.button_clear_entry_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        button_inverse.clicked.connect(lambda state, operation = "inverse": self.button_operation_clicked(operation))
        button_square.clicked.connect(lambda state, operation = "square": self.button_operation_clicked(operation))
        button_squ_root.clicked.connect(lambda state, operation = "root": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### 버튼을 layout_operation1 레이아웃에 추가
        layout_operation1.addWidget(button_rest, 0, 0)
        layout_operation1.addWidget(button_c_entry, 0, 1)
        layout_operation1.addWidget(button_clear, 0, 2)
        layout_operation1.addWidget(button_backspace, 0, 3)
        layout_operation1.addWidget(button_inverse, 1, 0)
        layout_operation1.addWidget(button_square, 1, 1)
        layout_operation1.addWidget(button_squ_root, 1, 2)
        layout_operation1.addWidget(button_division, 1, 3)

        layout_operation1.addLayout(layout_operation2, 2, 3, 1, 1)
        layout_operation1.addLayout(layout_number, 2, 0, 1, 3)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButtonNumber(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number > 0:
                x = int((( 9 - number ) / 3 ) + 1 )
                y = (( number - 1 ) % 3)
                print(str(number) + ' : ' + str(x) + ',' + str(y))
                layout_number.addWidget(number_button_dict[number], x-1, y, 1, 1)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 3, 1)

        ### reverse 버튼과 소숫점 버튼을 입력하고 시그널 설정
        button_reverse = QPushButtonNumber("+/-")
        button_reverse.clicked.connect(lambda state, num = "-1": self.button_reverse_clicked(num))
        layout_number.addWidget(button_reverse, 3, 0)

        button_dot = QPushButtonNumber(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 3, 2)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution, 0, 0)
        main_layout.addLayout(layout_operation1, 1, 0)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        if self.fin_calc != 0:
            self.equation.setText("")
        equation = self.equation.text()
        equation += str(num)
        self.fin_calc = 0
        self.equation.setText(equation)
        print('clicked num : ' + str(equation))

    def button_reverse_clicked(self, num):
        equation = self.equation.text()
        equation = str(float(equation) * -1)
        self.equation.setText(equation)
        print('reversed num : ' + str(equation))

    def button_operation_clicked(self, operation):
        print('operation : ' + operation)
        if operation not in ["square", "root", "inverse"]:
            self.temp_number = float(self.equation.text())
            self.equation.setText("")
            self.temp_operator = operation
            pass
        else:
            ### square, root, inverse 연산의 사칙 연산 - fix
            self.temp_another = float(self.equation.text())
            if operation == "square":
                self.temp_another = math.pow(self.temp_another, 2)
            if operation == "root":
                self.temp_another = math.sqrt(self.temp_another)
            if operation == "inverse":
                self.temp_another = np.reciprocal(self.temp_another)
            self.equation.setText(str(self.temp_another))
            self.fin_calc = 1
            print('changed num : ' + str(self.temp_another))
            self.temp_another = 0

    def button_equal_clicked(self):
        temp_second_number = float(self.equation.text())
        if self.temp_another != 0:
            self.temp_number = float(self.temp_another)
        if self.temp_operator == "+":
            temp_result = self.temp_number + temp_second_number
        if self.temp_operator == "-":
            temp_result = self.temp_number - temp_second_number
        if self.temp_operator == "*":
            temp_result = self.temp_number * temp_second_number
        if self.temp_operator == "/":
            ### 0 -> 창 닫힘 - fix
            if temp_second_number != 0.0:
                temp_result = self.temp_number / temp_second_number
            else:
                temp_result = '0으로 나눌 수 없습니다.'
        if self.temp_operator == "%":
            if temp_second_number != 0.0:
                temp_result = self.temp_number % temp_second_number
            else:
                temp_result = '0으로 나눌 수 없습니다.'

        self.equation.setText(str(temp_result))
        print('result : ' + str(temp_result))

        self.temp_operator = ""
        self.temp_number = 0
        self.temp_another = 0
        self.fin_calc = 1

    def button_clear_clicked(self):
        self.equation.setText("")

    def button_clear_entry_clicked(self):
        self.equation.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
