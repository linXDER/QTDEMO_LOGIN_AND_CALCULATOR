import sys
import datetime
import re
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from UI.calculator import Ui_Form


class Calculator(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        self.setupUi(self)
        for i in range(int(self.tableWidget.rowCount())):
            self.radio = QRadioButton()
            self.tableWidget.setCellWidget(i, 2, self.radio)
        self.i = 0

    """
    “+”按钮的槽函数
    """

    def plus_in_time(self):
        calculator_area_text = self.calculator_area.text()
        calculator_data_1_text = self.calculate_data_1.text()
        if len(calculator_area_text) > 0:
            if len(calculator_data_1_text) == 0:
                self.calculator_area.setText('')
                self.calculate_data_1.setText(calculator_area_text)

    """
    “=”按钮槽函数
    """

    def calculate(self):
        calculator_area_text = self.calculator_area.text()
        calculator_data_1_text = self.calculate_data_1.text()
        calculator_data_2_text = self.calculate_data_2.text()
        if len(calculator_data_1_text) > 0:
            if len(calculator_data_2_text) == 0:  # 当第二计算数据区域为零时，将输入区域的数据填入第二计算数据区
                self.calculate_data_2.setText(str(calculator_area_text))
                calculator_data_2_text = self.calculate_data_2.text()
            a = float(calculator_data_2_text) + float(calculator_data_1_text)
            self.calculator_area.setText(str(a))
            self.calculate_result.setText(str(a))
            self.count()
            self.plot_result()

    def plot_result(self):
        self.data_plot.mpl.start_plot(int(self.i), float(self.calculate_result.text()))

    """
    实时输入时绑定的函数
    """

    def clear_result(self):
        calculator_result_text = self.calculate_result.text()
        if len(calculator_result_text) > 0:
            q = QMessageBox.question(self, '确定', '数据尚未保存，是否放弃保存，进行新的运算？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if q == QMessageBox.Yes:
                self.clear_all_but_area()

    """
    计算表格内的数据，表格内的数据需要选中某一行数据
    """

    def calculate_data(self):
        for i in range(self.tableWidget.rowCount()):
            if (self.tableWidget.cellWidget(i, 2).isChecked()):
                if (len(self.tableWidget.item(i, 0).text()) > 0 and len(self.tableWidget.item(i, 1).text()) > 0):
                    self.calculate_data_1.setText(self.tableWidget.item(i, 0).text())
                    self.calculate_data_2.setText(self.tableWidget.item(i, 1).text())
                    self.tableWidget.cellWidget(i, 2).setChecked(0)
                    calculate_result_text = float(self.tableWidget.item(i, 0).text()) + float(
                        self.tableWidget.item(i, 1).text())
                    self.calculate_result.setText(str(calculate_result_text))
                    self.count()
                    self.plot_result()

    # def data_position(self):
    #     for i in range(self.tableWidget.rowCount()):
    #         if(self.tableWidget.cellWidget(i, 2).isChecked()):
    #             if(len(self.tableWidget.item(i, 0).text()) > 0 and len(self.tableWidget.item(i, 1).text())>0):
    #                 self.calculate_data_1.setText(self.tableWidget.item(i, 0).text())
    #                 self.calculate_data_2.setText(self.tableWidget.item(i, 1).text())
    #                 self.tableWidget.cellWidget(i, 2).setChecked(0)
    #                 calculate_result_text = int(self.tableWidget.item(i, 0).text())+int(self.tableWidget.item(i, 1).text())
    #                 self.calculate_result.setText(str(calculate_result_text))
    """
    建立以”data+年月日时分“为名的txt文件记录计算数据
    """

    def restore_data(self):
        restore_data_1 = self.calculate_data_1.text()
        restore_data_2 = self.calculate_data_2.text()
        restore_result = self.calculate_result.text()
        if (len(restore_data_1) != 0 and len(restore_data_2) != 0 and len(restore_result) != 0):
            time = str(datetime.datetime.now())
            time_new = re.sub('[- :.]', '', time)[0:11]  # 将得到的time变成纯数字形式，形式为20220817141，每10分钟将数据储存在新的txt文件
            get_path = QFileDialog.getExistingDirectory(self,
                                                        "选取指定文件夹",
                                                        "D:/")
            file_name = get_path + "/data" + time_new + ".txt"
            f = open(file_name, "a+")
            f.write(restore_data_1 + "+" + restore_data_2 + "=" + restore_result + '\n')
            f.close()

    """
    清空计算区域缓存的数据，在开始新一次运算的时候调用
    """

    def clear_all_but_area(self):
        self.calculate_data_1.setText('')
        self.calculate_data_2.setText('')
        self.calculate_result.setText('')

    """
    清空计算区域和输入区域的数据
    """

    def clear_all(self):
        if self.calculate_data_1.text() or self.calculate_data_2.text() or self.calculate_result.text():
            a = QMessageBox.question(self, '删除', '你确定要删除现有数据吗？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
            if a == QMessageBox.Yes:
                self.calculator_area.setText('')
                self.clear_all_but_area()

    """
    删除选中的数据行
    """

    def delete_data(self):
        for i in range(self.tableWidget.rowCount()):
            if (self.tableWidget.cellWidget(i, 2).isChecked()):
                if (len(self.tableWidget.item(i, 0).text()) > 0 and len(self.tableWidget.item(i, 1).text()) > 0):
                    self.tableWidget.item(i, 0).setText('')
                    self.tableWidget.item(i, 1).setText('')

    def count(self):
        self.i += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
