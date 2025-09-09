import platform
import shutil
from addnote import Ui_AddNote
from editnote import Ui_EditNoteDialog
from delnote import Ui_DelNote
from opennote import Ui_OpenNoteTwo
from mainwindowdaily import Ui_MainWindowDaily
from screeninfo import get_monitors
from PyQt5 import QtWidgets, QtCore
import sys
from datetime import datetime
import json
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLCDNumber,
    QDialog,
    QMainWindow,
    QListWidgetItem, QSizePolicy, QMenu
)
from PyQt5.QtCore import QDate, Qt, QTimer, QTime, QLocale
import subprocess
from PyQt5.QtGui import QTextCharFormat, QColor, QPixmap, QIcon
from PyQt5 import QtGui, QtWidgets
import os
from os import path

try:
    from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize

    print("Quartz imported успешно.")
except ImportError as e:
    print(f"Error importing Quartz: {e}")
from cryptography.fernet import Fernet, InvalidToken

def ensure_writable(file_path):
    if os.path.isfile(file_path):
        if platform.system() == "Windows":
            subprocess.run(["attrib", "-H", file_path], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(["chmod", "u+w", file_path], check=True)

def set_hidden(file_path):
    if os.path.isfile(file_path):
        if platform.system() == "Windows":
            subprocess.run(["attrib", "+H", file_path], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(["chmod", "u-w", file_path], check=True)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.abspath("."))
    return path.join(base_path, relative_path)

def get_app_data_path():
    if platform.system() == "Windows":
        return path.join(os.getenv('APPDATA'), 'Planner')
    elif platform.system() == "Darwin":  # macOS
        return path.join(path.expanduser("~"), 'Library', 'Application Support', 'Planner')
    else:  # Linux и другие UNIX-подобные системы11
        return path.join(path.expanduser("~"), '.config', 'Planner')

ENCRYPTION_KEY = b'aSO-mTaOE72BQS3Nm1hvX_yO5yDEHTYUI207oFYI8Cs='
fernet = Fernet(ENCRYPTION_KEY)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = ".data.json"
PASSWORD_FILE = ".password_data.json"

def set_hidden(file_path):
    if os.path.isfile(file_path):
        if platform.system() == "Windows":
            subprocess.run(["attrib", "+H", file_path], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(["chmod", "u-w", file_path], check=True)

def ensure_writable(file_path):
    if os.path.isfile(file_path):
        if platform.system() == "Windows":
            subprocess.run(["attrib", "-H", file_path], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(["chmod", "u+w", file_path], check=True)

def initialize_file(file_path):
    if not path.exists(file_path):
        ensure_writable(file_path)
        try:
            with open(file_path, 'w') as file:
                file.write("{}")
                print(f"Файл {file_path} инициализирован с пустым JSON объектом.")
        except PermissionError as e:
            print(f"Ошибка доступа к файлу: {e}")
        finally:
            set_hidden(file_path)

def copy_resources():
    app_data_path = get_app_data_path()
    os.makedirs(app_data_path, exist_ok=True)

    data_file_path = path.join(app_data_path, DATA_FILE)
    password_file_path = path.join(app_data_path, PASSWORD_FILE)

    if not path.exists(data_file_path):
        initialize_file(data_file_path)

    if not path.exists(password_file_path):
        initialize_file(password_file_path)

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

class PasswordDialog(QDialog):

    def __init__(self, is_first_time, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        self.setWindowIcon(QIcon(pixmap))
        if platform.system() == 'Darwin':
            from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
            width_dpi, height_dpi = get_screen_density_mac()
            average_dpi = (width_dpi + height_dpi) / 2
        else:
            width_dpi, height_dpi = get_screen_density_windows()
            average_dpi = (width_dpi + height_dpi) / 2
        self.setObjectName('enter_pass')
        self.is_first_time = is_first_time
        self.setWindowTitle('Установите пароль' if is_first_time else 'Вход')

        if platform.system() == 'Darwin':
            from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
            width_dpi, height_dpi = get_screen_density_mac()
            self.average_dpi = (width_dpi + height_dpi) / 2
        else:
            width_dpi, height_dpi = get_screen_density_windows()
            self.average_dpi = (width_dpi + height_dpi) / 2
        new_width = int(300 * (self.average_dpi / 127.5))
        new_height = int(150 * (self.average_dpi / 127.5))
        self.setFixedSize(new_width, new_height)
        font = QtGui.QFont("Verdana")
        self.setFont(font)
        self.setStyleSheet("#enter_pass {\n"
                           "background-color: #FCF1C9;"
                           f"font-size: {int(14 * (self.average_dpi / 127.5))}px"
                           "}"
                           "QPushButton {\n"
                           "background-color: #F4DF96;\n"
                           "border-radius: 9%;\n"
                           "border: 1px solid gray;\n"
                           f"width: {int(55 * (average_dpi / 127.5))}px;\n"
                           f"height: {int(25 * (average_dpi / 127.5))}px;\n"
                           "}\n"
                           "QPushButton:hover {\n"
                           "background-color: #dbb44b;\n"
                           "}")

        self.layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Установите пароль:' if is_first_time else 'Введите свой пароль:')
        self.label.setStyleSheet(f"font-weight: bold; font-size: {int(14 * (self.average_dpi / 127.5))}px;")
        self.layout.addWidget(self.label)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText('Oк')

        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText('Отмена')
        self.button_box.setStyleSheet(f"font-size: {int(13 * (self.average_dpi / 127.5))}px;")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def accept(self):
        if platform.system() == 'Darwin':
            from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
            width_dpi, height_dpi = get_screen_density_mac()
            average_dpi = (width_dpi + height_dpi) / 2
        else:
            width_dpi, height_dpi = get_screen_density_windows()
            average_dpi = (width_dpi + height_dpi) / 2
        password = self.get_password()
        if 4 <= len(password) <= 12:
            super().accept()
        else:
            msg = QtWidgets.QMessageBox()
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.transparent)
            msg.setWindowIcon(QIcon(pixmap))

            msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                              "QPushButton {\n"
                              "background-color: #F4DF96;\n"
                              "border-radius: 9%;\n"
                              "border: 1px solid gray;\n"
                              f"width: {int(55 * (average_dpi / 127.5))}px;\n"
                              f"height: {int(25 * (average_dpi / 127.5))}px;\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "background-color: #dbb44b;\n"
                              "}")
            msg.setText(
                f'<span style="font-weight:bold; font-size: {int(14 * (self.average_dpi / 127.5))}px;">Пароль должен содержать от 4 до 12 символов')
            msg.setWindowTitle('Ошибка')
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.transparent)
            msg.setWindowIcon(QIcon(pixmap))

            msg.exec_()

    def get_password(self):
        return self.password_input.text()

def save_password(password):
    # Save only non-empty passwords
    if password:
        encrypted_password = fernet.encrypt(password.encode()).decode()
        data = {'password': encrypted_password}
    else:
        data = {}
    
    ensure_writable(get_app_data_path())
    ensure_writable(PASSWORD_FILE)
    
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(data, file)
    
    if platform.system() == "Windows":
        subprocess.run(["attrib", "+H", PASSWORD_FILE], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(["attrib", "+H", get_app_data_path()], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.run(["chmod", "u-w", PASSWORD_FILE], check=True)
        subprocess.run(["chmod", "u-w", get_app_data_path()], check=True)

def load_password():
    if not path.exists(PASSWORD_FILE):
        return None
    with open(PASSWORD_FILE, 'r') as file:
        data = json.load(file)
    encrypted_password = data.get('password')
    if encrypted_password:
        try:
            return fernet.decrypt(encrypted_password.encode()).decode()
        except InvalidToken as e:
            print(f"Error decrypting password: {e}")
            return None
    return None

class AddNoteDialog(QDialog, Ui_AddNote):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(None))
        self.setWindowTitle("Добавление записи")

    def getInputs(self):
        mainNote = self.caption.text()
        additionalNote = self.description.toPlainText()
        return mainNote, additionalNote

    def reject(self):
        super().reject()

class DailyPlanner(QMainWindow, Ui_MainWindowDaily):
    currentDay = str(datetime.now().day).rjust(2, "0")
    currentMonth = str(datetime.now().month).rjust(2, "0")
    currentYear = str(datetime.now().year).rjust(2, "0")

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ежедневник")
        self.fix_width = 861
        self.fix_height = 490
        self.standard_dpi = 127.5
        if platform.system() == 'Darwin':
            from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
            width_dpi, height_dpi = get_screen_density_mac()
            self.average_dpi = (width_dpi + height_dpi) / 2
        else:
            width_dpi, height_dpi = get_screen_density_windows()
            self.average_dpi = (width_dpi + height_dpi) / 2
        self.new_width = int(self.fix_width * (self.average_dpi / self.standard_dpi))
        self.new_height = int(self.fix_height * (self.average_dpi / self.standard_dpi))
        self.setFixedSize(self.new_width, self.new_height)
        self.initUI()

    def initUI(self):

        self.fmt = QTextCharFormat()
        self.fmt.setBackground(QColor(255, 165, 0, 100))

        self.data = {}
        if path.isfile(DATA_FILE):
            with open(DATA_FILE, "r") as json_file:
                encrypted_data = json.load(json_file)
                try:
                    self.data = {date: [self.decrypt_data(note) for note in notes] for date, notes in
                                 encrypted_data.items()}
                except InvalidToken as e:
                    print(f"Error decrypting data: {e}")
                    self.data = {}

        self.cur_date = QDate.currentDate()

        for date in list(self.data.keys()):
            qdate = QDate.fromString(date, "ddMMyyyy")
            self.calendarWidget.setDateTextFormat(qdate, self.fmt)

        self.addButton = self.pushButton_3
        self.addButton.clicked.connect(self.addNote)

        self.editButton = self.pushButton_4
        self.editButton.clicked.connect(self.editNote)

        self.delButton = self.pushButton_5
        self.delButton.clicked.connect(self.delNote)

        self.pushButton_6.clicked.connect(change_pass)

        self.calendarWidget.selectionChanged.connect(self.showDateInfo)
        self.calendarWidget.selectionChanged.connect(self.labelDate)
        self.calendarWidget.selectionChanged.connect(self.highlightFirstItem)
        self.calendarWidget.selectionChanged.connect(self.toggleAddEditDeleteButtons)
        self.calendarWidget.selectionChanged.connect(self.updateDateInfo)

        todayButton = self.pushButton_2
        todayButton.clicked.connect(self.selectToday)

        self.label = self.label_date
        self.labelDate()
        self.showDateInfo()
        self.listView.itemDoubleClicked.connect(self.showFullNote)
        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listView.customContextMenuRequested.connect(self.contextMenuEvent)

        self.lcd = self.lcdNumber
        self.lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.lcd.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); color: white;")

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

    def contextMenuEvent(self, position):
        try:
            menu = QMenu()
            addPointerAction = menu.addAction("Закрепить/открепить заметку")
            action = menu.exec_(self.listView.viewport().mapToGlobal(position))

            if action == addPointerAction:
                self.togglePointerInNote()

        except Exception as e:
            print(f"Error: {e}")

    def togglePointerInNote(self):
        currentRow = self.listView.currentRow()
        if currentRow >= 0:
            date = self.getDate()
            note_data = self.data[date][currentRow]
            decrypted_note = self.decrypt_data(note_data)

            if decrypted_note.startswith("📌"):
                decrypted_note = decrypted_note[2:].strip()
            else:
                decrypted_note = "📌 " + decrypted_note

            encrypted_note = self.encrypt_data(decrypted_note)
            self.data[date][currentRow] = encrypted_note
            self.saveData()
            self.showDateInfo()

    def selectToday(self):
        self.calendarWidget.setSelectedDate(QDate.currentDate())

    def encrypt_data(self, data):
        return fernet.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        try:
            return fernet.decrypt(encrypted_data.encode()).decode()
        except InvalidToken as e:
            print(f"Error: {e}")
            return ""

    def addNote(self):
        dialog = QtWidgets.QDialog()
        ui = Ui_AddNote()
        ui.setupUi(dialog)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            mainNote, additionalNote = ui.getInputs()
            if not mainNote:
                return
            date = self.getDate()

            self.calendarWidget.setDateTextFormat(QDate.fromString(date, "ddMMyyyy"), self.fmt)

            note = f"{mainNote}: {additionalNote}" if additionalNote else mainNote
            encrypted_note = self.encrypt_data(note)
            if date in self.data:
                self.data[date].append(encrypted_note)
            else:
                self.data[date] = [encrypted_note]

            self.saveData()

            self.showDateInfo()

    def editNote(self):
        date = self.getDate()
        row = self.listView.currentRow()
        item = self.listView.item(row)

        if item:
            note_data = self.decrypt_data(self.data[date][row])
            mainNote, additionalNote = (note_data.split(":", 1) + [""])[
                                       :2]  

            if mainNote.startswith("📌"):
                mainNote = mainNote[2:].strip()

            dialog = QDialog()
            ui = Ui_EditNoteDialog()
            ui.setupUi(dialog)

            ui.caption.setPlainText(mainNote.strip())
            ui.description.setPlainText(additionalNote.strip())

            if dialog.exec_() == QDialog.Accepted:
                editedMainNote, editedAdditionalNote = ui.getInputs()
                editedMainNote = editedMainNote.strip()
                editedAdditionalNote = editedAdditionalNote.strip()
                if not editedMainNote:
                    return
                if note_data.startswith("📌"): 
                    editedMainNote = "📌 " + editedMainNote 
                editedNote = f"{editedMainNote}: {editedAdditionalNote}" if editedAdditionalNote else editedMainNote
                encrypted_note = self.encrypt_data(editedNote)

                self.data[date][row] = encrypted_note

                self.saveData()

                self.showDateInfo()

    def delNote(self):
        currentRow = self.listView.currentRow()
        if currentRow >= 0:
            item = self.listView.item(currentRow)
            if item:
                dialog = QDialog()
                ui = Ui_DelNote()
                ui.setupUi(dialog)
                if dialog.exec_() == QDialog.Accepted:
                    print("Запись удалена")
                    date = self.getDate()
                    print("Дата, для которой происходит удаление:", date)

                    self.listView.takeItem(currentRow)

                    if date in self.data:
                        del self.data[date][currentRow]
                        if not self.data[date]:
                            del self.data[date]
                            self.calendarWidget.setDateTextFormat(QDate.fromString(date, "ddMMyyyy"), QTextCharFormat())
                            self.listView.clear()

                    self.saveData()
                else:
                    print("Удаление отменено")

    def showDateInfo(self):
        date = self.getDate()
        self.listView.clear()
        new_width = int(401 * (self.average_dpi / self.standard_dpi))
        self.listView.setFixedWidth(new_width)

        pinned_notes = []
        regular_notes = []

        if date in self.data:
            for note in self.data[date]:
                decrypted_note = self.decrypt_data(note)
                if decrypted_note.startswith("📌"):
                    pinned_notes.append(decrypted_note)
                else:
                    regular_notes.append(decrypted_note)

            notes = pinned_notes + regular_notes

            self.data[date] = [self.encrypt_data(note) for note in notes]

            for note in notes:
                if ":" in note:
                    mainNote, additionalNote = note.split(":", 1)
                else:
                    mainNote, additionalNote = note, ""
                listItem, widget = createCustomListItem(str(mainNote), str(additionalNote))
                new_width = int(401 * (self.average_dpi / self.standard_dpi))
                widget.setFixedWidth(new_width)

                self.listView.addItem(listItem)
                self.listView.setItemWidget(listItem, widget)

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString("hh:mm")
        if time.second() % 2 == 0:
            text.replace(text[2], "")
        self.lcd.display(text)

    def getDate(self):
        select = self.calendarWidget.selectedDate()
        date = select.toString("ddMMyyyy")
        return date

    def closeEvent(self, e):
        self.saveData()
        e.accept()

    def saveData(self):
        ensure_writable(get_app_data_path())
        ensure_writable(DATA_FILE)
        
        with open(DATA_FILE, "w") as json_file:
            encrypted_data = {date: [self.encrypt_data(note) for note in notes] for date, notes in self.data.items()}
            json.dump(encrypted_data, json_file)
        
        if platform.system() == "Windows":
            subprocess.run(["attrib", "+H", DATA_FILE], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["attrib", "+H", get_app_data_path()], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(["chmod", "u-w", DATA_FILE], check=True)
            subprocess.run(["chmod", "u-w", get_app_data_path()], check=True)

    def labelDate(self):
        select = self.calendarWidget.selectedDate()
        self.label_date.setLocale(QLocale(QLocale.Russian))
        weekday, month = select.dayOfWeek(), select.month()
        day, year = str(select.day()), str(select.year())
        russian_locale = QLocale(QLocale.Russian, QLocale.Russia)
        week_day = russian_locale.dayName(weekday)
        word_month = russian_locale.monthName(month)
        self.label_date.setText(week_day + ", " + day + ' ' + word_month + "" ", " + year)

    def toggleAddEditDeleteButtons(self):
        enabled = self.calendarWidget.selectedDate() >= QDate.currentDate()
        for button in [self.addButton, self.editButton, self.delButton]:
            button.setEnabled(enabled)

    def showFullNote(self, item):
        note_data = item.data(Qt.UserRole)
        mainNote = note_data["mainNote"]
        additionalNote = note_data["additionalNote"]
        dialog = QtWidgets.QDialog()
        ui = Ui_OpenNoteTwo()
        ui.setupUi(dialog, mainNote, additionalNote)
        dialog.exec_()

    def highlightFirstItem(self):
        if self.listView.count() > 0:
            self.listView.setCurrentRow(0)

    def updateDateInfo(self):
        self.showDateInfo()

def createCustomListItem(mainNote, additionalNote, max_length=50):
    widget = QWidget()
    layout = QVBoxLayout(widget)

    mainNoteLabel = QLabel(mainNote)
    if platform.system() == 'Darwin':
        from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
        width_dpi, height_dpi = get_screen_density_mac()
        average_dpi = (width_dpi + height_dpi) / 2
    else:
        width_dpi, height_dpi = get_screen_density_windows()
        average_dpi = (width_dpi + height_dpi) / 2
    mainNoteLabel.setStyleSheet(
        f"font-family: Verdana; font-size: {int(15 * (average_dpi / 127.5))}px; font-weight: bold;")

    truncatedAdditionalNote = truncate_text(additionalNote, max_length)
    additionalNoteLabel = QLabel(truncatedAdditionalNote)
    additionalNoteLabel.setMaximumWidth(int(280 * (average_dpi / 127.5)))
    additionalNoteLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    additionalNoteLabel.setStyleSheet(f"""
        font-family: Verdana;
        font-size: {int(15 * (average_dpi / 127.5))}px;
        color: black;
        white-space: nowrap;
        margin: 0;
        padding: 0;
    """)

    layout.addWidget(mainNoteLabel)
    layout.addWidget(additionalNoteLabel)

    listItem = QListWidgetItem()
    listItem.setData(Qt.UserRole, {"mainNote": mainNote, "additionalNote": additionalNote})
    listItem.setSizeHint(widget.sizeHint())

    return listItem, widget

def truncate_text(text, max_length=50):
    lines = text.splitlines()
    if not lines:
        return ""

    first_line = lines[0].strip()

    if len(lines) == 1 and len(first_line) <= max_length:
        return first_line

    if len(first_line.split()) > 1 and len(first_line) > max_length:
        return first_line[:max_length - 3] + "..."

    return first_line[:max_length] + "..." if len(first_line) > max_length or len(lines) > 1 else first_line

def change_pass():
    if platform.system() == 'Darwin':
        from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
        width_dpi, height_dpi = get_screen_density_mac()
        average_dpi = (width_dpi + height_dpi) / 2
    else:
        width_dpi, height_dpi = get_screen_density_windows()
        average_dpi = (width_dpi + height_dpi) / 2
    dialog = PasswordDialog(is_first_time=True)
    if dialog.exec_() == QDialog.Accepted:
        user_password = dialog.get_password()

        if user_password:  
            save_password(user_password)
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                              "QPushButton {\n"
                              "background-color: #F4DF96;\n"
                              "border-radius: 9%;\n"
                              "border: 1px solid gray;\n"
                              f"width: {int(55 * (average_dpi / 127.5))}px;\n"
                              f"height: {int(25 * (average_dpi / 127.5))}px;\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "background-color: #dbb44b;\n"
                              "}")

            msg.setText(
                f'<span style="font-weight:bold; font-size:{int(14 * (average_dpi / 127.5))}px;">Пароль успешно установлен!</span>')
            msg.setWindowTitle('Успешно')
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.transparent)
            msg.setWindowIcon(QIcon(pixmap))

            msg.exec_()
        else:
            if path.exists(PASSWORD_FILE):
                ensure_writable(get_app_data_path())
                ensure_writable(PASSWORD_FILE)
                with open(PASSWORD_FILE, 'w') as file:
                    json.dump({}, file)
                    subprocess.run(["attrib", "+H", PASSWORD_FILE], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    subprocess.run(["attrib", "+H", get_app_data_path()], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                              "QPushButton {\n"
                              "background-color: #F4DF96;\n"
                              "border-radius: 9%;\n"
                              "border: 1px solid gray;\n"
                              f"width: {int(55 * (average_dpi / 127.5))}px;\n"
                              f"height: {int(25 * (average_dpi / 127.5))}px;\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "background-color: #dbb44b;\n"
                              "}")
            msg.setText('Пароль не установлен. Записи не будут защищены.')
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.transparent)
            msg.setWindowIcon(QIcon(pixmap))
            msg.setWindowTitle('Предупреждение')
            msg.exec_()
    else:
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                          "QPushButton {\n"
                          "background-color: #F4DF96;\n"
                          "border-radius: 9%;\n"
                          "border: 1px solid gray;\n"
                          f"width: {int(55 * (average_dpi / 127.5))}px;\n"
                          f"height: {int(25 * (average_dpi / 127.5))}px;\n"
                          "}\n"
                          "QPushButton:hover {\n"
                          "background-color: #dbb44b;\n"
                          "}")
        msg.setText(f'<span style="font-weight:bold;font-size:{int(14 * (average_dpi / 127.5))}px;">Изменение пароля отменено</span>')
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        msg.setWindowIcon(QIcon(pixmap))
        msg.setWindowTitle('Отмена')
        msg.exec_()

def main():
    copy_resources()
    if platform.system() == 'Darwin':
        from Quartz import CGDisplayBounds, CGMainDisplayID, CGDisplayScreenSize
        width_dpi, height_dpi = get_screen_density_mac()
        average_dpi = (width_dpi + height_dpi) / 2
    else:
        width_dpi, height_dpi = get_screen_density_windows()
        average_dpi = (width_dpi + height_dpi) / 2
    app = QApplication(sys.argv)
    saved_password = load_password()
    attempts = 3
    if saved_password is None:
        dialog = PasswordDialog(is_first_time=True)
        if dialog.exec_() == QDialog.Accepted:
            user_password = dialog.get_password()
            if user_password:
                save_password(user_password)
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                                  "QPushButton {\n"
                                  "background-color: #F4DF96;\n"
                                  "border-radius: 9%;\n"
                                  "border: 1px solid gray;\n"
                                  f"width: {int(55 * (average_dpi / 127.5))}px;\n"
                                  f"height: {int(25 * (average_dpi / 127.5))}px;\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "background-color: #dbb44b;\n"
                                  "}")
                msg.setText(
                    f'<span style="font-weight:bold; font-size:{int(14 * (average_dpi / 127.5))}px;">Пароль успешно установлен!</span>')
                msg.setWindowTitle('Успешно')
                pixmap = QPixmap(32, 32)
                pixmap.fill(Qt.transparent)
                msg.setWindowIcon(QIcon(pixmap))
                msg.exec_()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet("QMessageBox {background-color: #FCF1C9}\n"
                                  "QPushButton {\n"
                                  "background-color: #F4DF96;\n"
                                  "border-radius: 9%;\n"
                                  "border: 1px solid gray;\n"
                                  f"width: {int(55 * (average_dpi / 127.5))}px;\n"
                                  f"height: {int(25 * (average_dpi / 127.5))}px;\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "background-color: #dbb44b;\n"
                                  "}")
                msg.setText('Пароль не установлен. Записи не будут защищены.')
                msg.setWindowTitle('Предупреждение')
                msg.exec_()
            run_main_app(app)
        else:
            sys.exit(0)
    else:
        while attempts > 0:
            dialog = PasswordDialog(is_first_time=False)
            if dialog.exec_() == QDialog.Accepted:
                user_password = dialog.get_password()
                if user_password and user_password == saved_password:
                    run_main_app(app)
                    return
                else:
                    attempts -= 1
                    msg = QtWidgets.QMessageBox()
                    msg.setStyleSheet("QMessageBox {background-color: #FCF1C9;\n"
                                      f"height: {int(300 * (average_dpi / 127.5))}px\n"
                                      "}\n"
                                      "QPushButton {\n"
                                      "background-color: #F4DF96;\n"
                                      "border-radius: 9%;\n"
                                      "border: 1px solid gray;\n"
                                      f"width: {int(55 * (average_dpi / 127.5))}px;\n"
                                      f"height: {int(25 * (average_dpi / 127.5))}px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "background-color: #dbb44b;\n"
                                      "}")
                    msg.setText(
                        f'<span style="font-weight:bold; font-size:{int(14 * (average_dpi / 127.5))}px;">Неправильный пароль. Осталось {attempts} попыток</span>')
                    msg.setWindowTitle('Ошибка')
                    pixmap = QPixmap(32, 32)
                    pixmap.fill(Qt.transparent)
                    msg.setWindowIcon(QIcon(pixmap))
                    msg.exec_()
            else:
                sys.exit(0)

            if attempts == 0:
                clear_notes()
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet("QMessageBox {background-color: #FCF1C9;\n"
                                      f"height: {int(300 * (average_dpi / 127.5))}px\n"
                                      "}\n"
                                      "QPushButton {\n"
                                      "background-color: #F4DF96;\n"
                                      "border-radius: 9%;\n"
                                      "border: 1px solid gray;\n"
                                      f"width: {int(55 * (average_dpi / 127.5))}px;\n"
                                      f"height: {int(25 * (average_dpi / 127.5))}px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "background-color: #dbb44b;\n"
                                      "}")
                msg.setText(
                    f'<span style="font-weight:bold; font-size:{int(14 * (average_dpi / 127.5))}px;">Попытки закончились. Все ваши записи удалены</span>')
                msg.setWindowTitle('Ошибка')
                pixmap = QPixmap(32, 32)
                pixmap.fill(Qt.transparent)
                msg.setWindowIcon(QIcon(pixmap))
                msg.exec_()
                sys.exit(0)

def clear_notes():
    if path.exists(DATA_FILE):
        ensure_writable(get_app_data_path())
        ensure_writable(DATA_FILE)
        with open(DATA_FILE, 'w') as file:
            json.dump({}, file)
        if platform.system() == "Windows":
            subprocess.run(["attrib", "+H", DATA_FILE], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["attrib", "+H", get_app_data_path()], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(["chmod", "u-w", DATA_FILE], check=True)
            subprocess.run(["chmod", "u-w", get_app_data_path()], check=True)

    if path.exists(PASSWORD_FILE):
        ensure_writable(get_app_data_path())
        ensure_writable(PASSWORD_FILE)
        with open(PASSWORD_FILE, 'w') as file:
            json.dump({}, file)
        if platform.system() == "Windows":
            subprocess.run(["attrib", "+H", PASSWORD_FILE], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["attrib", "+H", get_app_data_path()], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(["chmod", "u-w", PASSWORD_FILE], check=True)
            subprocess.run(["chmod", "u-w", get_app_data_path()], check=True)

def run_main_app(app):
    russian_locale = QLocale(QLocale.Russian)
    QLocale.setDefault(russian_locale)
    planner = DailyPlanner()
    planner.show()
    app.exec()

if __name__ == "__main__":
    main()
