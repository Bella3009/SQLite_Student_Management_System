from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout,\
     QLineEdit, QPushButton
import sys
from datetime import datetime


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        date_label = QLabel("Date of Birth DD/MM/YYYY:")
        self.date_birth_edit = QLineEdit()

        calculate_btn = QPushButton("Calculate Age")
        calculate_btn.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        # Add widgets to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(date_label, 1, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(self.date_birth_edit, 1, 1)
        grid.addWidget(calculate_btn, 2, 0, 1, 2)  # (Widget name, Row, Column, Row Span, Col Span)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        birth_date = self.date_birth_edit.text()  # Without self Python cannot retrieve the data
        year_birth = datetime.strptime(birth_date, "%d/%m/%Y").date().year
        age = current_year - year_birth
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old.")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())
