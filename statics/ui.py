from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QDateEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtWidgets import QHeaderView

class StudentManagementUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Quản Lý Sinh Viên")
        self.setGeometry(200, 100, 1000, 800)

        # Main layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Hệ Thống Quản Lý Sinh Viên")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Input Fields
        form_layout = QHBoxLayout()
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Tên")
        self.name_input.setFont(QFont("Arial", 12))
        form_layout.addWidget(self.name_input)

        self.age_input = QLineEdit(self)
        self.age_input.setPlaceholderText("Tuổi")
        self.age_input.setFont(QFont("Arial", 12))
        form_layout.addWidget(self.age_input)

        self.class_input = QLineEdit(self)
        self.class_input.setPlaceholderText("Lớp")
        self.class_input.setFont(QFont("Arial", 12))
        form_layout.addWidget(self.class_input)

        self.date_time_edit = QDateEdit(self)
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.date_time_edit.setDisplayFormat("yyyy-MM-dd")
        form_layout.addWidget(self.date_time_edit)

        self.major_input = QLineEdit(self)
        self.major_input.setPlaceholderText("Ngành học")
        self.major_input.setFont(QFont("Arial", 12))
        form_layout.addWidget(self.major_input)

        self.gpa_input = QLineEdit(self)
        self.gpa_input.setPlaceholderText("Điểm")
        self.gpa_input.setFont(QFont("Arial", 12))
        form_layout.addWidget(self.gpa_input)

        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Thêm")
        self.add_button.setFont(QFont("Arial", 12))
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Cập nhật")
        self.update_button.setFont(QFont("Arial", 12))
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Xóa")
        self.delete_button.setFont(QFont("Arial", 12))
        button_layout.addWidget(self.delete_button)
        
        self.import_button = QPushButton("Nhập file excel")
        self.import_button.setFont(QFont("Arial", 12))
        button_layout.addWidget(self.import_button)

        self.export_button = QPushButton("Xuất file excel")
        self.export_button.setFont(QFont("Arial", 12))
        button_layout.addWidget(self.export_button)

        main_layout.addLayout(button_layout)

        # Table for displaying students
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(["Tên", "Tuổi", "Lớp", "Ngày sinh", "Ngành học", "Điểm"])
        self.student_table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.student_table)
        
        header = self.student_table.horizontalHeader()
        for i in range(self.student_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def populate_table(self, data):
        self.student_table.setRowCount(len(data))
        for row, student in enumerate(data):
            for col, value in enumerate(student):
                self.student_table.setItem(row, col, QTableWidgetItem(str(value)))


