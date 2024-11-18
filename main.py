# Tep chinh chay ung dung
# Khoi tao giao dien va su kien chinh
from database import Connect, AddStudent, GetStudent
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget
from statics.ui import StudentManagementUI

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = StudentManagementUI()
    window.show()
    sys.exit(app.exec())