from customtkinter import *
from database import collection, CheckValidValue, DataCorrector
from tkinter import *

# Giao diện CustomTkinter
app = CTk()
app.geometry("1920x1080")
app.title("Quản lý sinh viên")

def MaximizeWindow() -> None: 
    app.state('zoomed') 
app.after(1, MaximizeWindow)

table_frame = CTkScrollableFrame(master=app)
table_frame.pack(pady=(80, 20), padx=20, fill="both", expand=True)

add_window = None
edit_window = None 
delete_window = None
sort_window = None
search_window = None

sort_column = StringVar() 
sort_column.set("MSSV")
sort_option = StringVar()
sort_option.set("Ascending Sort")

def PrintTitle() -> None:
    headers: list = [
        ("MSSV", 1, 100), ("Họ đệm", 2, 180), ("Tên", 3, 80), ("Giới tính", 4, 90), 
        ("Lớp", 5, 90), ("Ngày sinh", 6, 120), ("Email", 7, 240), ("Số TC đã có", 8, 100), 
        ("Tổng học phí", 9, 180), ("Học phí đã đóng", 10, 180), ("Còn nợ", 11, 180), ("Ghi chú", 12, 290)
    ]
    for text, column, width in headers:
        header = CTkLabel(
            master=table_frame, text=text, width=width, height=30, 
            fg_color="grey", text_color="black", corner_radius=5, font=("Arial", 13, "bold")
        )
        header.grid(row=0, column=column, padx=1, pady=1, sticky="nsew")

def SelectRow(row) -> None:
    global selected_row
    if selected_row != row:
        selected_row = row
        UpdateRowColors()


def UpdateRowColors() -> None:
    global selected_row
    for widget in table_frame.winfo_children():
        # Kiểm tra nếu widget là CTkFrame và có thuộc tính 'row'
        if isinstance(widget, CTkFrame) and 'row' in widget.grid_info():
            row = int(widget.grid_info()['row'])
            if row % 2 == 1:
                widget.configure(fg_color="teal" if selected_row == row else "transparent")
selected_row = None
        
def PrintElement(data, row) -> None:
    global selected_row
    fields = [
        ("mssv", 1, 100), ("hodem", 2, 180), ("name", 3, 80), ("gender", 4, 90), 
        ("class", 5, 90), ("birth", 6, 120), ("email", 7, 240), ("owned_cert", 8, 100), 
        ("tuition", 9, 180), ("payed", 10, 180), ("debt", 11, 180), ("note", 12, 290)
    ]
    
    for field, column, width in fields:
        label_text = str(data.get(field, ""))
        if field in ["tuition", "payed", "debt"]:
            label_text += " VNĐ"
        
        frame_bg = "teal" if selected_row == row else "transparent"
        row_frame = CTkFrame(master=table_frame, width=width, height=30, fg_color=frame_bg)
        #Căn chỉnh frame nền row được chọn không bị thừa ở 2 bên
        if field == "mssv":  
            row_frame.grid(row=row, column=column, padx=(2,1), pady=1, sticky="ew")
        elif field == "note":
            row_frame.grid(row=row, column=column, padx=(1,2), pady=1, sticky="ew")
        else:
            row_frame.grid(row=row, column=column, padx=1, pady=1, sticky="ew")

        label = CTkLabel(master=row_frame, text=label_text, width=width, height=30)
        label.place(relx=0.5, rely=0.5, anchor="center")

        label.bind("<Button-3>", lambda e, d=data, r=row: ShowContextMenu(e, d))
        label.bind("<Button-1>", lambda e, r=row: SelectRow(r))
        label.bind("<Button-3>", lambda e, r=row: SelectRow(r))

context_menu = None

def ShowContextMenu(event, data) -> None:
    global context_menu

    if context_menu is not None:
        context_menu.destroy()

    # Tạo menu tùy chỉnh
    context_menu = CTkFrame(app, corner_radius=8, fg_color="#333333")
    context_menu.place(x=event.x_root, y=event.y_root)

    # Nút Chỉnh sửa
    edit_button = CTkButton(
        master=context_menu,
        text="Chỉnh sửa",
        command=lambda: [OpenEditDataWindow(data), context_menu.destroy()],
        fg_color="#444444",
        hover_color="#555555",
        text_color="white",
        corner_radius=8,
        width=100
    )
    edit_button.pack(padx=10, pady=5)

    # Nút Xóa
    delete_button = CTkButton(
        master=context_menu,
        text="Xóa",
        command=lambda: [OpenDeleteDataWindow(data), context_menu.destroy()],
        fg_color="#444444",
        hover_color="#555555",
        text_color="white",
        corner_radius=8,
        width=100
    )
    delete_button.pack(padx=10, pady=(0,5))

    # Hàm đóng menu
    def CloseContextMenu(event):
        global context_menu
        if context_menu is not None:
            context_menu.destroy()
            context_menu = None
    app.bind("<Button-1>", CloseContextMenu)


def RefreshTable(documents=list(collection.find())) -> None:
    # Xóa các widget hiện tại trong `table_frame` (nếu có)
    for widget in table_frame.winfo_children():
        widget.grid_forget()  # Chỉ ẩn các widget thay vì xóa
    PrintTitle()

    try:
        
        # Hiển thị dữ liệu lên giao diện
        for idx, document in enumerate(documents):
            PrintElement(document, idx * 2 + 1)  # Hiển thị dòng dữ liệu
            separator = CTkFrame(master=table_frame, fg_color="#cccccc", height=2)
            separator.grid(row=idx * 2 + 2, column=0, columnspan=13, sticky="ew", padx=3, pady=0)
    except Exception as e:
        print("Error: ", e)

def OpenAddDataWindow() -> None:
    global add_window

    if add_window and add_window.winfo_exists():
        add_window.focus()
        return

    add_window = CTkToplevel(app)
    add_window.title("Thêm dữ liệu")
    add_window.geometry("700x310+660+400")
    add_window.attributes('-topmost', True)

    def AddData():
        data = {
            "mssv": mssv_entry.get(),
            "hodem": hodem_entry.get(),
            "name": name_entry.get(),
            "gender": gender_entry.get(),
            "class": class_entry.get(),
            "birth": birth_entry.get(),
            "email": email_entry.get(),
            "owned_cert": owned_cert_entry.get(),
            "tuition": tuition_entry.get(),
            "payed": payed_entry.get(),
            "note": note_entry.get(),
        }


        # Check if any field (except `debt`) is empty
        if not all(data[key] for key in data if key not in ["debt"]):
            error_label.configure(text="Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Check for 
        tuition: str = data["tuition"]
        payed: str = data["payed"]
        name: str = data["name"]
        second_name: str = data["hodem"]
        email: str = data["email"]
        id: str = data["mssv"]

        error_text = CheckValidValue(id, name, second_name, email, tuition, payed)

        if error_text != "":
            error_label.configure(text=error_text)
            error_text = ""
            return
         
        # Add the calculated `debt` to the data dictionary
        data["debt"] = int(data["tuition"]) - int(data["payed"])

        DataCorrector(data)

        try:
            collection.insert_one(data)  # Add data to MongoDB
            error_label.configure(text="Dữ liệu đã được thêm!")
        except Exception as e:
            error_label.configure(text=f"Lỗi: {e}")

    def CreateEntry(label_text, row, column):
        label = CTkLabel(master=add_window, text=label_text)
        label.grid(row=row, column=column, padx=(20, 5), pady=5)
        entry = CTkEntry(master=add_window, width=200)
        entry.grid(row=row, column=column + 1, padx=5, pady=5)
        return entry

    mssv_entry = CreateEntry("MSSV:", 0, 0)
    hodem_entry = CreateEntry("Họ đệm:", 1, 0)
    name_entry = CreateEntry("Tên:", 2, 0)
    gender_entry = CreateEntry("Giới tính:", 3, 0)
    class_entry = CreateEntry("Lớp:", 4, 0)
    birth_entry = CreateEntry("Ngày sinh:", 5, 0)
    email_entry = CreateEntry("Email:", 0, 2)
    owned_cert_entry = CreateEntry("Số TC đã có:", 1, 2)
    tuition_entry = CreateEntry("Tổng học phí:", 2, 2)
    payed_entry = CreateEntry("Học phí đã đóng:", 3, 2)
    note_entry = CreateEntry("Ghi chú:", 4, 2)

    add_button = CTkButton(master=add_window, text="Thêm", command=AddData)
    add_button.grid(row=11, column=1, padx=20, pady=10)

    cancel_button = CTkButton(master=add_window, text="Xong", command=add_window.destroy)
    cancel_button.grid(row=11, column=3, padx=5, pady=10)

    error_label = CTkLabel(master=add_window, text="", text_color="red")
    error_label.grid(row=12, column=1, padx=0, pady=0)


# Hàm mở cửa sổ chỉnh sửa dữ liệu
def OpenEditDataWindow(data) -> None:
    global edit_window
    if edit_window and edit_window.winfo_exists():
        edit_window.focus()
        return

    edit_window = CTkToplevel(app)
    edit_window.title("Chỉnh sửa dữ liệu")
    edit_window.geometry("700x310+660+400")
    edit_window.attributes('-topmost', True)

    def UpdateData():
        updated_data = {
            "mssv": mssv_entry.get(),
            "hodem": hodem_entry.get(),
            "name": name_entry.get(),
            "gender": gender_entry.get(),
            "class": class_entry.get(),
            "birth": birth_entry.get(),
            "email": email_entry.get(),
            "owned_cert": owned_cert_entry.get(),
            "tuition": tuition_entry.get(),
            "payed": payed_entry.get(),
            "note": note_entry.get(),
        }


        # Check if any field (except `debt`) is empty
        if not all(updated_data[key] for key in updated_data if key not in ["debt"]):
            error_label.configure(text="Vui lòng nhập đầy đủ thông tin!")
            return

        tuition = updated_data["tuition"]
        payed = updated_data["payed"]
        name = updated_data["name"]
        second_name = updated_data["hodem"]
        email: str = updated_data["email"]
        id = updated_data["mssv"]
        _id = data["_id"]
        error_text = CheckValidValue(id, name, second_name, email, tuition, payed, _id)

        if error_text != "":
            error_label.configure(text=error_text)
            error_text = ""
            return

        # Add the calculated `debt` to the updated_data dictionary
        updated_data["debt"] = int(updated_data["tuition"]) - int(updated_data["payed"])
        DataCorrector(updated_data)
        try:
            collection.update_one({"_id": data["_id"]}, {"$set": updated_data})
            error_label.configure(text="Dữ liệu đã được cập nhật!")

            document = list(collection.find())
            RefreshTable(document)
        except Exception as e:
            error_label.configure(text=f"Lỗi: {e}")
        

    def CreateEntry(label_text, initial_value, row, column):
        label = CTkLabel(master=edit_window, text=label_text)
        label.grid(row=row, column=column, padx=(20, 5), pady=5)
        entry = CTkEntry(master=edit_window, width=200)
        entry.insert(0, initial_value)
        entry.grid(row=row, column=column + 1, padx=5, pady=5)
        return entry

    mssv_entry = CreateEntry("MSSV:", data.get("mssv", ""), 0, 0)
    hodem_entry = CreateEntry("Họ đệm:", data.get("hodem", ""), 1, 0)
    name_entry = CreateEntry("Tên:", data.get("name", ""), 2, 0)
    gender_entry = CreateEntry("Giới tính:", data.get("gender", ""), 3, 0)
    class_entry = CreateEntry("Lớp:", data.get("class", ""), 4, 0)
    birth_entry = CreateEntry("Ngày sinh:", data.get("birth", ""), 5, 0)
    email_entry = CreateEntry("Email:", data.get("email", ""), 0, 2)
    owned_cert_entry = CreateEntry("Số TC đã có:", data.get("owned_cert", ""), 1, 2)
    tuition_entry = CreateEntry("Tổng học phí:", data.get("tuition", ""), 2, 2)
    payed_entry = CreateEntry("Học phí đã đóng:", data.get("payed", ""), 3, 2)
    note_entry = CreateEntry("Ghi chú:", data.get("note", ""), 4, 2)

    update_button = CTkButton(master=edit_window, text="Cập nhật", command=UpdateData)
    update_button.grid(row=11, column=1, padx=20, pady=10)

    cancel_button = CTkButton(master=edit_window, text="Xong", command=edit_window.destroy)
    cancel_button.grid(row=11, column=3, padx=5, pady=10)

    error_label = CTkLabel(master=edit_window, text="", text_color="red")
    error_label.grid(row=12, column=1, columnspan=2)

def OpenDeleteDataWindow(data) -> None:
    global delete_window
    # Kiểm tra nếu cửa sổ con đã mở thì không tạo thêm
    if delete_window and delete_window.winfo_exists():
        delete_window.focus()
        return

    delete_window = CTkToplevel(app)
    delete_window.title("Xóa dữ liệu")
    delete_window.geometry("400x100+660+400")
    delete_window.attributes('-topmost', True)
    def DeleteData():
        collection.delete_one(data)

        delete_window.destroy()
    label = CTkLabel(master=delete_window,text= "Bạn có chắc chắn muốn xóa người này?", anchor="center")
    label.grid(row=1,column=0, pady = 5, padx = 10)

    confirm_button = CTkButton(master=delete_window, text="OK", command=DeleteData)
    confirm_button.grid(row=2, column=0, padx=10, pady=10, sticky="e") 

    cancel_button = CTkButton(master=delete_window, text="Hủy", command=delete_window.destroy)
    cancel_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

def OpenSortDataWindow():
    global sort_window
    if sort_window and sort_window.winfo_exists():
        sort_window.focus()
        return
    
    sort_window = CTkToplevel(app)
    sort_window.title("Sắp xếp")
    sort_window.geometry("350x130+660+400")
    sort_window.attributes('-topmost', True)
    display_value = {
        "MSSV": "mssv",
        "Họ đệm": "hodem",
        "Tên": "name",
        "Lớp": "class",
        "Giới tính": "gender",
        "Ngày sinh": "birth",
        "Email": "email",
        "Số TC đã có": "owned_cert",
        "Tổng học phí": "tuition",
        "Học phí đã đóng": "payed",
        "Còn nợ": "debt",
        "Ghi chú": "note"
        }
    sort_option_display = {
        "Ascending Sort": 1,
        "Descending Sort": -1
    }
    label = CTkLabel(master=sort_window,text="Chọn thuộc tính cần sắp xếp")
    label.grid(row=1,column=0, pady = 5, padx = 10)
    sort_column_combobox = CTkComboBox(master=sort_window, values=list(display_value.keys()), variable=sort_column)
    sort_column_combobox.grid(row=2,column=0, pady = 5, padx = 10)

    sort_option_combobox = CTkComboBox(master=sort_window, values=list(sort_option_display.keys()), variable=sort_option)
    sort_option_combobox.grid(row=2,column=1, pady = 5, padx = 10)

    def sort_database() -> None:
        document = collection.find().sort({display_value[sort_column.get()]: sort_option_display[sort_option.get()]})
        RefreshTable(document)
        sort_window.destroy()

    confirm_button = CTkButton(master=sort_window, text="OK", command=sort_database)
    confirm_button.grid(row=3, column=0, padx=10, pady=10, sticky="e") 

    cancel_button = CTkButton(master=sort_window, text="Hủy", command=sort_window.destroy)
    cancel_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

def OpenSearchDataWindow() -> None:
    global search_window
    if search_window and search_window.winfo_exists():
        search_window.focus()
        return
    search_window = CTkToplevel(app)
    search_window.title("Tìm kiếm")
    search_window.geometry("350x130+660+400")
    search_window.attributes('-topmost', True)

    label = CTkLabel(master=search_window,text="Nhập từ khóa cần tìm:")
    label.grid(row = 0, column= 0, pady = 5, padx = 10)
    entry = CTkEntry(master=search_window, width= 240)
    entry.grid(row = 1, column= 0, pady = 5, padx = (20, 5))



buttons_data = [
    {"image_path": r"template/add_student.png", "command": OpenAddDataWindow, "x": 20, "size": (20, 20)},
    {"image_path": r"template/sort.png", "command": OpenSortDataWindow, "x": 75, "size": (20, 20)},
    {"image_path": r"template/search.png", "command": OpenSearchDataWindow, "x": 130, "size": (30, 30)},
    {"image_path": r"template/refresh.png", "command": lambda: RefreshTable(documents=list(collection.find())), "x": 185, "size": (30, 30)},
]

for button in buttons_data:
    image = PhotoImage(file=button["image_path"]).subsample(*button["size"])
    CTkButton(
        master=app,
        text="",
        image=image,
        command=button["command"],
        width=50,
        height=60,
        fg_color="#444444",
        hover_color="gray",
        border_width=2,
        border_color="black"
    ).place(x=button["x"], y=10)

# Hiển thị tiêu đề và dữ liệu ban đầu
PrintTitle()
RefreshTable()

app.mainloop()
