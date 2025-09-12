from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, \
     QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
     QVBoxLayout, QComboBox, QToolBar, QStatusBar, QGridLayout, QLabel, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3

# класс для подключения к базе данных
class DatabaseConnection:
    def __init__(self, database_file="lab1/database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


# главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("lab1/icons/add.png"), "Добавить студета", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("lab1/icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        # таблица для отображения студентов
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # тулбар с быстрыми кнопками
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # отслеживаем клик по ячейке таблицы
        self.table.cellClicked.connect(self.cell_clicked)


    def cell_clicked(self):
        # при клике на ячейку показываем кнопки редактирования и удаления в статусбаре
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # чистим предыдущие кнопки
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # добавляем новые кнопки
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        # загружаем данные студентов из базы в таблицу
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        # открываем окно добавления студента
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        # открываем окно поиска
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        # открываем окно редактирования
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        # открываем окно удаления
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This was created only for practice. 
        Feel free to modify and reuse this app.
        """
        self.setText(content)

# окно редактирования студента
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # берем данные выбранного студента из таблицы
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        self.student_id = main_window.table.item(index, 0).text()

        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Register")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        # обновляем данные студента в базе
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                                   self.course_name.itemText(self.course_name.currentIndex()),
                                   self.mobile.text(),
                                   self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        # обновляем таблицу
        main_window.load_data()

# окно подтверждения удаления
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        # удаляем студента из базы
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        
        # обновляем таблицу и показываем сообщение об успехе
        main_window.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()

# окно добавления нового студента
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавления данных студента")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Имя")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Телефон")
        layout.addWidget(self.mobile)

        button = QPushButton("Добавить")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        # добавляем нового студента в базу
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        
        # обновляем таблицу
        main_window.load_data()

# окно поиска студентов
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поиск студента")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Имя или первая буква")
        layout.addWidget(self.student_name)

        button = QPushButton("Поиск")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        # ищем студентов по имени или первой букве
        search_text = self.student_name.text().strip().lower()
        
        if not search_text:
            QMessageBox.information(self, "Input Error", "Please enter a name or letter to search.")
            return
        
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        
        # ищем в базе студентов с именем начинающимся на введенный текст
        result = cursor.execute("SELECT * FROM students WHERE LOWER(name) LIKE ?", (f"{search_text}%",))
        
        rows = result.fetchall()
        
        if not rows:
            QMessageBox.information(self, "Not Found", f"No student found starting with '{search_text}'.")
            cursor.close()
            connection.close()
            return
        
        # подсвечиваем найденных студентов в таблице
        main_window.table.clearSelection()
        found_count = 0
        
        for row_idx in range(main_window.table.rowCount()):
            item = main_window.table.item(row_idx, 1) 
            if item and item.text().lower().startswith(search_text):
                found_count += 1
                for col_idx in range(main_window.table.columnCount()):
                    main_window.table.item(row_idx, col_idx).setSelected(True)
                if found_count == 1:
                    main_window.table.scrollToItem(item)
        
        cursor.close()
        connection.close()

# запуск приложения
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())