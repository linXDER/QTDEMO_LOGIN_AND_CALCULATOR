import sys

from PyQt5.QtWidgets import QApplication, QWidget
from calculator_pane import Calculator
from UI.login import Ui_Form



class Login(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)

    """
    检查输入的账号密码是否符合命名规矩
    """
    def check_login(self):
        account_text = self.name_line.currentText()
        password_text = self.password_line.text()
        if 6 <= len(account_text) <= 10 and len(password_text) > 8 and 100000 < int(account_text) < 100000000000:
            self.login_btn.setEnabled(True)
        else:
            self.login_btn.setEnabled(False)

    """
    如果账号密码输入正确，打开计算界面
    """
    def checked_login(self):
        account_text = self.name_line.currentText()
        password_text = self.password_line.text()
        if account_text == "1234567890" and password_text == '123456789':
            calculator_pane.show()
            login.hide()
        else:
            self.login_state.setText("账号或密码错误,登录失败")

    """
    记住密码与自动登录按钮的槽函数，暂未开发功能
    仅实现选择自动登录时自动勾选记住密码
    不记住密码时不能选择自动登录
    """
    def rember_pwd(self, checked):
        if not checked:
            self.antologin_checkbox.setChecked(False)

    def auto_login(self, checked):
        if checked:
            self.rember_checkbox.setChecked(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    calculator_pane = Calculator()
    login.show()
    sys.exit(app.exec())
