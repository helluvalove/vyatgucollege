import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QTextBrowser
from screeninfo import get_monitors

try:
    from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize

    print("Quartz imported successfully.")
except ImportError as e:
    print(f"Error importing Quartz: {e}")
class DynamicFontLabel(QtWidgets.QLabel):
    def __init__(self, *args, max_width=200, **kwargs):
        super().__init__(*args, **kwargs)
        if platform.system() == 'Darwin':
            from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
            width_dpi, height_dpi = get_screen_density_mac()
            self.average_dpi = (width_dpi + height_dpi) / 2
        else:
            width_dpi, height_dpi = get_screen_density_windows()
            self.average_dpi = (width_dpi + height_dpi) / 2
        self.max_width = max_width
        self.adjust_font_size()

    def adjust_font_size(self):
        font = QtGui.QFont("Verdana")
        font_metrics = QtGui.QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(self.text())
        while text_width > self.max_width and font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            self.setFont(font)
            font_metrics = QtGui.QFontMetrics(font)
            text_width = font_metrics.horizontalAdvance(self.text())
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
                           "border-radius: 10%;\n"
                           "border: 1px solid gray;\n"
                           "}\n"
                           "QPushButton:hover {\n"
                           "background-color: #dbb44b;\n"
                           "}")

class Ui_OpenNoteTwo(object):
    def __init__(self):
        if platform.system() == 'Darwin':
            from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
            width_dpi, height_dpi = get_screen_density_mac()
            self.average_dpi = (width_dpi + height_dpi) / 2
        else:
            width_dpi, height_dpi = get_screen_density_windows()
            self.average_dpi = (width_dpi + height_dpi) / 2

    def setupUi(self, MainWindow, MainNote, AdditionalNote):
        self.Main_note = MainNote
        self.Addit_note = AdditionalNote
        font = QtGui.QFont("Verdana")
        font_label = QtGui.QFont("Verdana")
        font_label.setBold(True)
        button_font = QtGui.QFont("Verdana")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(int(438 * (self.average_dpi / 127.5)), int(320 * (self.average_dpi / 127.5)))
        MainWindow.setStyleSheet("#MainWindow {\n"
                                 "background-color: #FCF1C9;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setFont(font)

        self.centralwidget.setStyleSheet("#centralwidget {\n"
                                         f"font-size: {int(16 * (self.average_dpi / 127.5))}px;\n"
                                         "background-color: #FCF1C9;\n"
                                         "}")
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = HighlightButton(MainWindow)
        self.pushButton.setFont(button_font)

        self.pushButton.setGeometry(
            QtCore.QRect(int(360 * (self.average_dpi / 127.5)), int(280 * (self.average_dpi / 127.5)),
                         int(61 * (self.average_dpi / 127.5)), int(30 * (self.average_dpi / 127.5))))
        self.pushButton.setObjectName("pushButton")
        self.label = DynamicFontLabel(self.centralwidget, max_width=int(401 * (self.average_dpi / 127.5)))
        font = (QtGui.QFont("Verdana"))
        font.setBold(True)
        self.label.setFont(font)

        self.label.setGeometry(QtCore.QRect(int(17 * (self.average_dpi / 127.5)), int(30 * (self.average_dpi / 127.5)),
                                            int(401 * (self.average_dpi / 127.5)),
                                            int(21 * (self.average_dpi / 127.5))))
        self.label.setObjectName("label")
        self.label.setStyleSheet("#label {\n"
                                 f"font-size: {int(14.5 * (self.average_dpi / 127.5))}px;\n"
                                 "background-color: #FCF1C9;\n"
                                 "}")


        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setFont(font)

        self.scrollArea.setGeometry(
            QtCore.QRect(int(20 * (self.average_dpi / 127.5)), int(70 * (self.average_dpi / 127.5)),
                         int(401 * (self.average_dpi / 127.5)), int(201 * (self.average_dpi / 127.5))))
        self.scrollArea.setStyleSheet("#scrollArea{\n"
                                      "border: None;\n"
                                      f"font-size: {int(14.5 * (self.average_dpi / 127.5))}px;\n"
                                      "background-color: #E32636;\n"
                                      "}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setFont(font)
        self.scrollAreaWidgetContents.setGeometry(
            QtCore.QRect(0, 0, int(401 * (self.average_dpi / 127.5)), int(201 * (self.average_dpi / 127.5))))
        self.scrollAreaWidgetContents.setStyleSheet("#scrollAreaWidgetContents{\n"
                                                    "border: None;\n"
                                                    f"font-size: {int(14.5 * (self.average_dpi / 127.5))}px;\n"
                                                    "background-color: transparent;\n"
                                                    "}")
        self.scrollAreaWidgetContents.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents)  
        font.setBold(False)
        self.textBrowser.setFont(font)
        self.textBrowser.setGeometry(
            QtCore.QRect(0, 0, int(401 * (self.average_dpi / 127.5)), int(201 * (self.average_dpi / 127.5))))
        self.textBrowser.setStyleSheet("#textBrowser{\n"
                                       "border: None;\n"
                                       "background-color: #FFFFFF;\n"
                                       f"font-size: {int(14 * (self.average_dpi / 127.5))}px;\n"
                                       "border: 1px solid gray;\n"
                                       "}")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setOpenExternalLinks(False)  
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(MainWindow.accept)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Просмотр заметки"))
        MainWindow.setFixedSize(int(438 * (self.average_dpi / 127.5)), int(320 * (self.average_dpi / 127.5)))
        self.pushButton.setText(_translate("MainWindow", "ОК"))
        self.label.setText(_translate("MainWindow", self.Main_note))

        if not self.Addit_note:
            self.scrollArea.hide()
            self.textBrowser.hide()
            self.pushButton.setGeometry(
                QtCore.QRect(int(320 * (self.average_dpi / 127.5)), int(80 * (self.average_dpi / 127.5)),
                             int(61 * (self.average_dpi / 127.5)), int(30 * (self.average_dpi / 127.5))))
            MainWindow.setFixedSize(int(400 * (self.average_dpi / 127.5)), int(120 * (self.average_dpi / 127.5)))
        else:
            self.textBrowser.setPlainText(self.Addit_note)
            self.pushButton.setGeometry(
                QtCore.QRect(int(360 * (self.average_dpi / 127.5)), int(280 * (self.average_dpi / 127.5)),
                             int(61 * (self.average_dpi / 127.5)), int(30 * (self.average_dpi / 127.5))))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_OpenNoteTwo()
    ui.setupUi(MainWindow, "Main Note", "Additional Note")
    MainWindow.show()
    sys.exit(app.exec_())
