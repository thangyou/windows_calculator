import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "계산기"
        self.setWindowTitle(self.title)
        self.init_ui()

    def init_ui(self):
        ### 레이아웃 설정
        main_layout = QGridLayout()
        layout_equation_solution = QGridLayout()
        layout_operation1 = QGridLayout() # 추가 연산
        layout_operation2 = QGridLayout() # 기본 연산
        layout_number = QGridLayout()

        self.temp_number = 0
        self.temp_operator = ""
        self.fin_calc = 0 # 계산 완료 상태 변수 (False)

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 통합 - issue #10
        layout_equation_solution = QGridLayout()
        self.equation = QLineEdit("")
        layout_equation_solution.addWidget(self.equation)

        ### 연산 버튼
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_equal = QPushButton("=")

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
        button_rest = QPushButton("%")
        button_clear = QPushButton("C") # Clear All
        button_c_entry = QPushButton("CE") # Clear last char
        button_backspace = QPushButton("Backspace")

        button_inverse = QPushButton("1/x") # 역수
        button_square = QPushButton("x²") # 제곱
        button_squ_root = QPushButton("²√x") # 제곱근
        button_division = QPushButton("/")

        ### 버튼 클릭 시 시그널 설정
        # button_rest.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_clear.clicked.connect(self.button_clear_clicked)
        button_c_entry.clicked.connect(self.button_clear_entry_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)
        #
        # button_inverse.clicked.connect(self.button_inverse_clicked)
        # button_square.clicked.connect(self.button_square_clicked)
        # button_squ_root.clicked.connect(self.button_squ_root_clicked)
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
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number > 0:
                x,y = divmod(number-1, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 3, 1)

        ### reverse 버튼과 소숫점 버튼을 입력하고 시그널 설정
        button_reverse = QPushButton("+/-")
        button_reverse.clicked.connect(lambda state, num = "-1": self.button_reverse_clicked(num))
        layout_number.addWidget(button_reverse, 3, 0)

        button_dot = QPushButton(".")
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
            print('비워랏')
            self.equation.setText("")
        equation = self.equation.text()
        equation += str(num)
        self.fin_calc = 0
        self.equation.setText(equation)
        # if solution != "":
        #     self.equation.setText("")
        # equation = self.equation.text()
        # equation += str(num)
        # self.equation.setText(equation)
        # global tmp
        # tmp = equation
        # print('num : ' + tmp)

    def button_reverse_clicked(self, num):
        equation = self.equation.text()
        equation = str(int(equation) * -1)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        if operation not in ["square", "root", "inverse"]:
            print('operation : ' + operation)
            self.temp_number = float(self.equation.text())
            self.equation.setText("")
            self.temp_operator = operation
        else:
            if operation == "square":
                pass
            if operation == "root":
                pass
            if operation == "inverse":
                pass

            self.temp_operator = ""
            self.temp_number = 0
        # print('operation : ' + operation)
        # print('tmp : ', tmp)
        # global final
        # final = tmp
        # self.equation.setText("")
        # global op
        # op = operation

    def button_equal_clicked(self):
        # equation = self.equation.text()
        # solution = eval(equation)
        # self.equation.setText(str(solution))
        temp_second_number = float(self.equation.text())

        if self.temp_operator == "+":
            temp_result = self.temp_number + temp_second_number
        if self.temp_operator == "-":
            temp_result = self.temp_number - temp_second_number
        if self.temp_operator == "*":
            temp_result = self.temp_number * temp_second_number
        if self.temp_operator == "/":
            temp_result = self.temp_number / temp_second_number

        self.equation.setText(str(temp_result))

        self.temp_operator = ""
        self.temp_number = 0
        self.fin_calc = 1

        # print('num1 : ' + final)
        # print('num2 : ' + tmp)
        # print('final math : ' + op)
        # global solution
        # if op == '+':
        #     if '.' in tmp or '.' in final:
        #         solution = str(float(tmp) + float(final))
        #     else:
        #         solution = str(int(final) + int(tmp))
        # if op == '-':
        #     if '.' in tmp or '.' in final:
        #         solution = str(float(tmp) - float(final))
        #     else:
        #         solution = str(int(final) - int(tmp))
        # if op == '*':
        #     if '.' in tmp or '.' in final:
        #         solution = str(float(tmp) * float(final))
        #     else:
        #         solution = str(int(final) * int(tmp))
        # if op == '/':
        #     if '.' in tmp or '.' in final:
        #         solution = str(float(tmp) / float(final))
        #     else:
        #         solution = str(int(final) / int(tmp))
        # if op == '%':
        #     if '.' in tmp or '.' in final:
        #         solution = str(float(tmp) % float(final))
        #     else:
        #         solution = str(int(final) % int(tmp))
        # print('solution : ' + solution)
        # self.equation.setText(str(solution))

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
