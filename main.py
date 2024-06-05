from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys, demo_ui, create_class, create_controller, create_view, schema_info,export_table_schema


class myMainWindow(QMainWindow, demo_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.txt_ProjectName.setText("CreateObjectByPython")
        self.btn_Create.clicked.connect(lambda: self.button_event())
        self.lbl_msg.setStyleSheet("QLabel { color: rgb(255, 0, 0); }")

        dt = schema_info.GetTableList()        
        self.comboBox.addItem("--All--")
        for row in dt:
            self.comboBox.addItem(row["TABLE_NAME"])

    def button_event(self):

        project_name = self.txt_ProjectName.text()
        table_name =  self.comboBox.currentText()
        try:  # 使用 try，測試內容是否正確
            create_class.Create(project_name,table_name)
            create_controller.Create(project_name,table_name)
            create_view.Create(project_name,table_name)
            create_view.Create(project_name,table_name)
            export_table_schema.Export(table_name)
            self.lbl_msg.setText("專案 %s 物件建立完成" % (project_name))
        except:  # 如果 try 的內容發生錯誤，就執行 except 裡的內容
            self.lbl_msg.setText("發生錯誤")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = myMainWindow()
    window.show()
    sys.exit(app.exec_())

