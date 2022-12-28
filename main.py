import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from math import prod, isqrt


class PostavtePyat(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)
        self.size = (-100, 100)
        self.setWindowTitle('Считатель квадртатного уравнения с корнями без иррациональности')

        self.A.textChanged.connect(self.calculate)
        self.B.textChanged.connect(self.calculate)
        self.C.textChanged.connect(self.calculate)

    def run(self, txt):
        self.grafen.clear()
        self.grafen.plot([i for i in range(*self.size)], [eval(f"{txt}") for x in range(*self.size)], pen='r')
        self.grafen.setRange(xRange=self.size, yRange=self.size)

    def calculate(self):
        try:
            a, b, c = int(self.A.text()), int(self.B.text()), int(self.C.text())
            txt = f'{a}*x**2 + {b}*x + {c}'
            ans = b ** 2 - 4 * a * c
            self.D.setText(f'{b ** 2} - 4 * {a} * {c} = {ans}')
            d = self.find_divs(ans)
            if ans > 0:
                self.amount.setText('2')
                self.x1.setText(f"X1 = {self.find_sq(a, b, d, 1)}")
                self.x2.setText(f"X2 = {self.find_sq(a, b, d, -1)}")
            elif ans == 0:
                self.amount.setText('1')
                self.x1.setText(f"X = {self.find_sq(a, b, d, 1)}")
                self.x2.setText(f"")
            else:
                self.amount.setText('Уравнение не имеет корней')
            self.run(txt)
        except Exception:
            self.amount.setText('Ошибка')

    @staticmethod
    def find_sq(a, b, d, p):
        half1 = str(-b / (2 * a))
        half1 = float(half1) if len((half1.split('.')[1])) <= 3 else f'({-b})/{2 * a}'
        half2 = f'({d})/{2 * a}' if '√' in d else float(d) / (2 * a)
        ans = f"{half1} {'+' if p == 1 else '-'} {half2}" if type(half1) is str or type(half2) is str else str(half1 + p * half2)
        return ans

    @staticmethod
    def find_divs(ans: float):
        divs, out_div = [], []
        for i in range(2, 10):
            while ans % i == 0:
                divs.append(i)
                ans //= i
        divs.append(ans)
        for i in divs:
            while divs.count(i) >= 2:
                for _ in range(2):
                    out_div.append(divs.pop(divs.index(i)))
        sq = f"√{str(prod(divs))}" if prod(divs) != 1 else ''
        return str(isqrt(prod(out_div))) + sq


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = PostavtePyat()
    ex.show()
    sys.exit(app.exec_())
