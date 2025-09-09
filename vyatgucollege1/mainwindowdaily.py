import os
import platform
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QPushButton
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

def resources_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HighlightButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setStyleSheet("#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover, #pushButton_6:hover {\n"
                            "background-color: #dbb44b;\n"
                            "}")

class Ui_MainWindowDaily(object):
    def __init__(self):
        self.average_dpi = None

    def setupUi(self, MainWindow):
        icon = QtGui.QIcon(resources_path("planner.png"))
        MainWindow.setWindowIcon(icon)
        if platform.system() == 'Darwin':
            from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
            width_dpi, height_dpi = get_screen_density_mac()
            self.average_dpi = (width_dpi + height_dpi) / 2
        else:
            width_dpi, height_dpi = get_screen_density_windows()
            self.average_dpi = (width_dpi + height_dpi) / 2
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(int(900 * (self.average_dpi / 127.5)), int(500 * (self.average_dpi / 127.5)))
        font = QtGui.QFont("Verdana")
        button_font = QtGui.QFont("Verdana")
        label_font = QtGui.QFont("Verdana")
        MainWindow.setFont(font)
        self.centralWidget = QtWidgets.QWidget(MainWindow)  
        self.centralWidget.setStyleSheet("#centralwidget {\n"
"background-color: #FCF1C9;\n"
"}")
        self.centralWidget.setObjectName("centralwidget")
        self.centralWidget.setFont(font)  
        self.pushButton_2 = HighlightButton(self.centralWidget)  
        self.pushButton_2.setFont(button_font)  
        self.pushButton_2.setGeometry(QtCore.QRect(int(440 * (self.average_dpi / 127.5)), int(20 * (self.average_dpi / 127.5)), int(111 * (self.average_dpi / 127.5)), int(41 * (self.average_dpi / 127.5))))
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setMouseTracking(False)
        self.pushButton_2.setStyleSheet("#pushButton_2 {\n"
                                "background-color: #F4DF96;\n"
                                "border-radius:15%;\n"
                                "border: 1px solid gray;\n"
                                "}")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_6 = HighlightButton(self.centralWidget)
        self.pushButton_6.setFont(button_font)
        self.pushButton_6.setGeometry(QtCore.QRect(int(440 * (self.average_dpi / 127.5)), int(430 * (self.average_dpi / 127.5)), int(300 * (self.average_dpi / 127.5)), int(35 * (self.average_dpi / 127.5))))
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_6.setMouseTracking(False)
        self.pushButton_6.setStyleSheet("#pushButton_6 {\n"
                                        "background-color: #F4DF96;\n"
                                        "border-radius:15%;\n"
                                        "border: 1px solid gray;\n"
                                        "}")
        self.pushButton_6.setObjectName("pushButton_6")

        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralWidget) 
        self.calendarWidget.setLocale(QLocale(QLocale.Russian))
        self.calendarWidget.setDateEditEnabled(False)
        self.calendarWidget.setGeometry(QtCore.QRect(int(20 * (self.average_dpi / 127.5)), int(20 * (self.average_dpi / 127.5)), int(401 * (self.average_dpi / 127.5)), int(401 * (self.average_dpi / 127.5))))
        self.calendarWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.calendarWidget.setToolTip("")
        self.calendarWidget.setStatusTip("")
        self.calendarWidget.setAutoFillBackground(True)

        self.calendarWidget.setStyleSheet("#calendarWidget QWidget {\n"
"    alternate-background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_navigationbar {\n"
"    background-color: #fff;\n"
"    border: 2px solid #F4DF96;\n"
"    border-bottom: 0px;\n"
"    border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth,\n"
"#qt_calendar_nextmonth {\n"
"    border: none;\n"
"\n"
"    min-width: 13px;\n"
"    max-width: 13px;\n"
"    min-height: 13px;\n"
"    max-height: 13px;\n"
"\n"
"    border-radius: 5px;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth {\n"
"    margin-left: 5px;\n"
"}\n"
"\n"
"#qt_calendar_nextmonth {\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth:hover,\n"
"#qt_calendar_nextmonth:hover {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth:pressed,\n"
"#qt_calendar_nextmonth:pressed {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton {\n"
"    color:#000;\n"
"    margin: 5px;\n"
"    border-radius: 5px;\n"
f"    font-size: {int(13 * (self.average_dpi / 127.5))}px;\n"
"    padding: 0 10px;\n"
"}\n"
"\n"
"#qt_calendar_monthbutton {\n"
"    width: 110px;\n"
"    color: #000;\n"
f"    font-size: {int(14 * (self.average_dpi / 127.5))}px;\n"
"    margin: 5px 0;\n"
"    border-radius: 5px;\n"
"    padding: 0px 2px;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton:hover,\n"
"#qt_calendar_monthbutton:hover {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton:pressed,\n"
"#qt_calendar_monthbutton:pressed {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#qt_calendar_yearedit {\n"
"    min-width: 53px;\n"
"    color: #000;\n"
"    background: transparent;\n"
f"    font-size: {int(13 * (self.average_dpi / 127.5))}px;\n"
"}\n"
"\n"
"\n"
"#calendarWidget QToolButton QMenu {\n"
"    background-color: #F4DF96;\n"
"}\n"
"\n"
"#calendarWidget QToolButton QMenu::item {\n"
"    /* padding: 5px; */\n"
"}\n"
"\n"
"#calendarWidget QToolButton QMenu::itemselected:enabled {\n"
"     background-color: #F4DF96;\n"
"}\n"
"\n"
"#calendarWidget QToolButton::menu-indicator {\n"
"    subcontrol-position: right center;\n"
"    margin-top: 10px;\n"
"    width: 20px;\n"
"}\n"
"\n"
"#qt_calendar_calendarview {\n"
"    border: 2px solid #F4DF96;\n"
"    border-top: 0px;\n"
"    border-bottom-left-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"}\n"
"\n"
"#qt_calendar_calendarview::item:hover {\n"
"    border-radius: 5px;\n"
"    background-color: #aaffff;\n"
"}\n"
"\n"
"#qt_calendar_calendarview::item:selected {\n"
"    border-radius: 5px;\n"
"    background-color: #F4DF96;\n"
"}")
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setObjectName("calendarWidget")
        self.pushButton_3 = HighlightButton(self.centralWidget)  
        self.pushButton_3.setFont(button_font) 
        self.pushButton_3.setGeometry(QtCore.QRect(int(440 * (self.average_dpi / 127.5)), int(380 * (self.average_dpi / 127.5)), int(121 * (self.average_dpi / 127.5)), int(41 * (self.average_dpi / 127.5))))
        self.pushButton_3.setStyleSheet("#pushButton_3 {\n"
"background-color: #F4DF96;\n"
"border-radius:15%;\n"
"border: 1px solid gray;\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = HighlightButton(self.centralWidget)  
        self.pushButton_4.setFont(button_font)  
        self.pushButton_4.setGeometry(QtCore.QRect(int(580 * (self.average_dpi / 127.5)), int(380 * (self.average_dpi / 127.5)), int(121 * (self.average_dpi / 127.5)), int(41 * (self.average_dpi / 127.5))))
        self.pushButton_4.setStyleSheet("#pushButton_4 {\n"
"background-color: #F4DF96;\n"
"border-radius:15%;\n"
"border: 1px solid gray;\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = HighlightButton(self.centralWidget)  
        self.pushButton_5.setFont(button_font) 
        self.pushButton_5.setGeometry(QtCore.QRect(int(720 * (self.average_dpi / 127.5)), int(380 * (self.average_dpi / 127.5)), int(121 * (self.average_dpi / 127.5)), int(41 * (self.average_dpi / 127.5))))
        self.pushButton_5.setStyleSheet("#pushButton_5 {\n"
"background-color: #F4DF96;\n"
"border-radius:15%;\n"
"border: 1px solid gray;\n"
"}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_date = QtWidgets.QLabel(self.centralWidget) 
        self.label_date.setLocale(QLocale(QLocale.Russian))
        self.label_date.setFont(label_font)
        self.label_date.setGeometry(QtCore.QRect(int(580 * (self.average_dpi / 127.5)), int(20 * (self.average_dpi / 127.5)), int(251 * (self.average_dpi / 127.5)), int(41 * (self.average_dpi / 127.5))))
        self.label_date.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_date.setObjectName("label")
        self.label_date.setStyleSheet(f"font-size: {int(17 * (self.average_dpi / 127.5))}px;")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralWidget)  
        self.lcdNumber.setFont(font)  
        self.lcdNumber.setGeometry(QtCore.QRect(int(770 * (self.average_dpi / 127.5)), int(430 * (self.average_dpi / 127.5)), int(64 * (self.average_dpi / 127.5)), int(23 * (self.average_dpi / 127.5))))
        self.lcdNumber.setMinimumWidth(int(80 * (self.average_dpi / 127.5)))
        self.lcdNumber.setObjectName("lcdNumber")
        self.scrollArea = QtWidgets.QScrollArea(self.centralWidget)  
        self.scrollArea.setFont(font)
        self.scrollArea.setGeometry(QtCore.QRect(int(440 * (self.average_dpi / 127.5)), int(70 * (self.average_dpi / 127.5)), int(401 * (self.average_dpi / 127.5)), int(291 * (self.average_dpi / 127.5))))
        self.scrollArea.setStyleSheet("#scrollArea {\n"
"border-radius: 70%;\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents = QtWidgets.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setFont(font)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, int(401 * (self.average_dpi / 127.5)), int(291 * (self.average_dpi / 127.5))))
        self.scrollAreaWidgetContents.setStyleSheet("#scrollAreaWidgetContents {\n"
"border-radius: 50%;\n"
"}")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.listView = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listView.setFont(font)  
        self.listView.setGeometry(QtCore.QRect(0, 0, int(401 * (self.average_dpi / 127.5)), int(291 * (self.average_dpi / 127.5))))
        self.listView.setStyleSheet("""
        QListView::item {\n"
        f"    height: {int(401 * (self.average_dpi / 127.5))}px;"
        }
        QListView {
            border: 1px solid gray;
            border-width: 1px;
            border-color: rgba(0,0,0,80);
        }
    """)
        self.listView.setObjectName("listView")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralWidget)
        self.listView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ежедневник"))
        self.pushButton_2.setText(_translate("MainWindow", "Сегодня"))
        self.pushButton_3.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_4.setText(_translate("MainWindow", "Изменить"))
        self.pushButton_5.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_6.setText(_translate("MainWindow", "Изменить пароль"))
        self.label_date.setText(_translate("MainWindow", "Суббота, Апрель 20, 2024"))

    def enterEvent(self, event):
        self.setStyleSheet("#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover, #pushButton_6:hover {\n"
                        "background-color: #F8E71C;\n"
                        "}"
                           
                        "#pushButton_2 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}"
                           
                        "#pushButton_3 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}" 
                           
                        "#pushButton_4 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}"
                           
                        "#pushButton_5 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"
                        "}"
                           
                        "#pushButton_6 {\n"
                        "background-color: #F4DF96;\n"
                        "border-radius:15%;\n"
                        "border: 1px solid gray;\n"   
                        "}"
)