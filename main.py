from PyQt6.QtWidgets import QApplication, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
    QLineEdit, QPushButton, QComboBox, QToolBar, QStatusBar

from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management Systems")
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        # Add main menu items
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        # Add submenu items
        add_student = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student.triggered.connect(self.insert)
        file_menu.addAction(add_student)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Add the view of data in table form
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add toolbar elements
        toolbar.addAction(add_student)

        # Create status bar and status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_btn = QPushButton("Edit Record")
        edit_btn.clicked.connect(self.edit)

        delete_btn = QPushButton("Delete Record")
        delete_btn.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        # Avoid showing the buttons more than ones
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_btn)
        self.statusbar.addWidget(delete_btn)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Find the data selected in the main window
        index = main_window.table.currentRow()
        self.student_id = main_window.table.item(index, 0).text()
        student_name = main_window.table.item(index, 1).text()  # row index, column index
        course_name = main_window.table.item(index, 2).text()
        mobile_num = main_window.table.item(index,3).text()

        # Add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box for courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile number widget
        self.mobile_num = QLineEdit(mobile_num)
        self.mobile_num.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_num)

        # Add a submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        # Display the Widgets in the window
        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile_num.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        # Refresh table
        main_window.load_data()


class DeleteDialog(QDialog):
    pass


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile number widget
        self.mobile_num = QLineEdit()
        self.mobile_num.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_num)

        # Add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        # Display the Widgets in the window
        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_num.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES(?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
