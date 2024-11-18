from customtkinter import *
from pymongo import MongoClient
import certifi

# Kết nối đến MongoDB Atlas
connection_string = "mongodb+srv://giahuy11095:123123123@hyper.kxke3.mongodb.net/"
client = MongoClient(connection_string, tlsCAFile=certifi.where())

db = client["test_db"]  # Truy cập database "test_db"
collection = db["test_collection"]  # Truy cập collection "test_collection"

# Giao diện CustomTkinter
app = CTk()
app.geometry("800x600")

table_frame = CTkFrame(master=app)
table_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Hàm hiển thị tiêu đề
def PrintTitle():
    header_ten = CTkLabel(master=table_frame, text="Tên", width=100, height=30, fg_color="gray70", corner_radius=5)
    header_ten.grid(row=0, column=1, padx=1, pady=1, sticky="nsew")
    
    header_tuoi = CTkLabel(master=table_frame, text="Tuổi", width=100, height=30, fg_color="gray70", corner_radius=5)
    header_tuoi.grid(row=0, column=2, padx=1, pady=1, sticky="nsew")
    
    header_email = CTkLabel(master=table_frame, text="Email", width=200, height=30, fg_color="gray70", corner_radius=5)
    header_email.grid(row=0, column=3, padx=1, pady=1, sticky="nsew")

# Hàm hiển thị dữ liệu từ MongoDB
def PrintElement(data, row):
    name_label = CTkLabel(master=table_frame, text=data.get("name", ""), width=100, height=30, corner_radius=5)
    name_label.grid(row=row, column=1, padx=1, pady=1)

    age_label = CTkLabel(master=table_frame, text=data.get("age", ""), width=100, height=30, corner_radius=5)
    age_label.grid(row=row, column=2, padx=1, pady=1)

    email_label = CTkLabel(master=table_frame, text=data.get("email", ""), width=200, height=30, corner_radius=5)
    email_label.grid(row=row, column=3, padx=1, pady=1)

# Hiển thị tiêu đề
PrintTitle()

# Hiển thị dữ liệu từ MongoDB
for idx, document in enumerate(collection.find()):
    PrintElement(document, idx + 1)

app.mainloop()

# Đóng kết nối MongoDB
client.close()
