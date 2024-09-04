import sys
import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QPushButton
from screeninfo import get_monitors
try:
    from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
    print("Quartz imported successfully.")
except ImportError as e:
    print(f"Error importing Quartz: {e}")

def get_screen_density_windows():
    monitors = get_monitors()
    for monitor in monitors:
        width_mm = monitor.width_mm  
        height_mm = monitor.height_mm  
        width_px = monitor.width  
        height_px = monitor.height 

        width_dpi = (width_px / (width_mm / 25.4))
        height_dpi = (height_px / (height_mm / 25.4))

        return width_dpi, height_dpi

def get_screen_density_mac():
    display_id = CGMainDisplayID()
    display_bounds = CGDisplayBounds(display_id)
    display_width_px = display_bounds.size.width
    display_height_px = display_bounds.size.height
    display_size_mm = CGDisplayScreenSize(display_id)
    display_width_mm = display_size_mm.width
    display_height_mm = display_size_mm.height

    width_dpi = (display_width_px / (display_width_mm / 25.4))
    height_dpi = (display_height_px / (display_height_mm / 25.4))

    return width_dpi, height_dpi

class HighlightButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        
        self.setStyleSheet("QPushButton {\n"
                            "background-color: #F4DF96;\n"
                            "border-radius: 15%;\n"
                            "border: 1px solid gray;\n"
                            "}\n"
                            "QPushButton:hover {\n"
                            "background-color: #dbb44b;\n"
                            "}")
        
class Ui_DelNote(object):
    def __init__(self):
        if platform.system() == 'Darwin':
            from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
            width_dpi, height_dpi = get_screen_density_mac()
            self.average_dpi = (width_dpi + height_dpi) / 2
        else:
            width_dpi, height_dpi = get_screen_density_windows()
            self.average_dpi = (width_dpi + height_dpi) / 2

    def setupUi(self, Dialog):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        Dialog.setWindowIcon(QIcon(pixmap))
        Dialog.setWindowFlags(Dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        Dialog.setObjectName("Dialog")
        Dialog.resize(int(350 * (self.average_dpi / 127.5)), int(112 * (self.average_dpi / 127.5)))
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: #FCF1C9;\n"
"}")
        font = QtGui.QFont("Verdana")
        button_font = QtGui.QFont("Verdana")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(int(43 * (self.average_dpi / 127.5)), int(20 * (self.average_dpi / 127.5)), int(401 * (self.average_dpi / 127.5)), int(31 * (self.average_dpi / 127.5))))
        self.label.setFont(font)
        self.label.setStyleSheet(
            f"font-size: {int(15 * (self.average_dpi / 127.5))}px;")
        self.label.setObjectName("label")
        self.pushButton = HighlightButton(Dialog)
        self.pushButton.setFont(button_font)
        self.pushButton.setGeometry(QtCore.QRect(int(180 * (self.average_dpi / 127.5)), int(60 * (self.average_dpi / 127.5)), int(71 * (self.average_dpi / 127.5)), int(31 * (self.average_dpi / 127.5))))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Dialog.reject)
        self.pushButton_2 = HighlightButton(Dialog)
        self.pushButton_2.setFont(button_font)

        self.pushButton_2.setGeometry(QtCore.QRect(int(260 * (self.average_dpi / 127.5)), int(60 * (self.average_dpi / 127.5)), int(71 * (self.average_dpi / 127.5)), int(31 * (self.average_dpi / 127.5))))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(Dialog.accept)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Удаление заметки"))
        Dialog.setFixedSize(int(350 * (self.average_dpi / 127.5)),int(112 * (self.average_dpi / 127.5)))
        self.label.setText(_translate("Dialog", "Вы точно хотите удалить эту запись?"))
        self.pushButton.setText(_translate("Dialog", "Нет"))
        self.pushButton_2.setText(_translate("Dialog", "Да"))

    def enterEvent(self, event):
        self.setStyleSheet("#pushButton:hover, #pushButton_2:hover {\n"
                        "background-color: #dbb44b;\n"
                        "}"
                        "#pushButton {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}"
                        "#pushButton_2 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}" )



