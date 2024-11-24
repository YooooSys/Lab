from customtkinter import *
import customtkinter
from database import collection, log_collection, ValueValidality, DataCorrector, Log, CopyDataFieldNo_ID, Search
from tkinter import *

# Giao diện CustomTkinter
customtkinter.set_appearance_mode("dark")
app = CTk()
app.geometry("1920x1080")
app.title("Quản lý sinh viên")

def MaximizeWindow() -> None: 
    app.state('zoomed') 

app.minsize(1300, 500)
app.after(1, MaximizeWindow)

# Color
grey_ = "#313338"
lighter_grey_ = "#3f4248"
text_color = "#c3c6ca"
text_color_onClick = "#f5f4e7"
darker_grey_ = "#1e1f22"
red_ = "#da373c"
# Table of content
header_frame = CTkFrame(master=app, height=30, fg_color=lighter_grey_)
header_frame.pack(expand=True, pady=(80, 0), padx=20, fill="both")

table_frame = CTkScrollableFrame(master=app, height=1000, fg_color=grey_)
table_frame.pack(expand=True, pady=(0, 20), padx=20, fill="both")


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
        ("MSSV", 0, 100), ("Họ đệm", 1, 180), ("Tên", 2, 85), ("Giới tính", 3, 90), 
        ("Lớp", 4, 90), ("Ngày sinh", 5, 120), ("Email", 6, 240), ("Số TC đã có", 7, 100), 
        ("Tổng học phí", 8, 180), ("Học phí đã đóng", 9, 180), ("Còn nợ", 10, 180), ("Ghi chú", 11, 290)
    ]
    for text, column, width in headers:
        header = CTkLabel(
            master=header_frame, text=text, width=width, height=30, 
            font=("Arial", 15, "bold")
        )
        if text == "MSSV":
            header.grid(row=0, column=column, padx=(5,1), pady=0, sticky="nsew")
        elif text == "Ghi chú":
            header.grid(row=0, column=column, padx=1, pady=0, sticky="nsew")
        else:
            header.grid(row=0, column=column, padx=1, pady=0, sticky="nsew")

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
                widget.configure(fg_color=lighter_grey_ if selected_row == row else "transparent")
selected_row = None
        
def PrintElement(data, row, highlight_list) -> None:
    global selected_row
    fields = [
        ("mssv", 0, 98), ("hodem", 1, 180), ("name", 2, 84), ("gender", 3, 94), 
        ("class", 4, 90), ("birth", 5, 118), ("email", 6, 240), ("owned_cert", 7, 104), 
        ("tuition", 8, 180), ("payed", 9, 180), ("debt", 10, 180), ("note", 11, 284)
    ]
    frame_bg = lighter_grey_ if selected_row == row else "transparent"
    row_frame = CTkFrame(
        master=table_frame,
        fg_color=frame_bg,
    )
    row_frame.grid(row=row, padx=0, pady=0, sticky="nsew")
    
    for field, column, width in fields:
        label_text = str(data.get(field, ""))
        if field in ["tuition", "payed", "debt"]:
            label_text += " VNĐ"

        label_bg = darker_grey_ if field in highlight_list else "transparent"

        label = CTkLabel(
            master=row_frame,
            text=label_text,
            width=width,
            height=35,
            fg_color=label_bg,
            text_color=text_color
        )
        label.grid(row=0, column=column, padx=1, pady=1, sticky="nsew")
        row_frame.columnconfigure(column, weight=1)

        label.bind("<Button-3>", lambda e, d=data, r=row: ShowContextMenu(e, d))
        label.bind("<Button-1>", lambda e, r=row: SelectRow(r))
        label.bind("<Button-3>", lambda e, r=row: SelectRow(r))

notificate_msg = None

def RefreshTable(documents=None) -> None:
    if documents == None:
        documents = list(collection.find())
    # Xóa các widget hiện tại trong `table_frame` (nếu có)
    for widget in table_frame.winfo_children():
        widget.grid_forget()  # Chỉ ẩn các widget thay vì xóa
    PrintTitle()
    try:
        # Hiển thị dữ liệu lên giao diện
        for idx, document in enumerate(documents):
            if len(search_result) == 0:
                PrintElement(document, idx * 2 + 1, [])  # Hiển thị dòng dữ liệu
            else:
                PrintElement(document, idx * 2 + 1, search_result[idx])
    except Exception as e:
        print("Error: ", e)

notificate_msg_height = 0

def Notificate(msg: str) -> None:
    global notificate_msg

    notificate_msg = CTkFrame(app, fg_color=lighter_grey_, corner_radius=8)

    label = CTkLabel(master=notificate_msg, text=msg, text_color=text_color)
    label.grid(padx=10, pady=10)

    x = app.winfo_width() / 2 - 100
    y = app.winfo_height() - 100


    notificate_msg.place(x=x, y=y)
    notificate_msg.after(3000, notificate_msg.destroy)


context_menu = None
context_menu_height = 0
def ShowContextMenu(event, data) -> None:
    global context_menu
    
    if context_menu is not None:
        context_menu.destroy()

    # Tạo menu tùy chỉnh
    context_menu = CTkFrame(app, corner_radius=8, fg_color=lighter_grey_, width=120)

    # Lấy vị trí
    x = event.x_root - app.winfo_x()
    y = event.y_root - app.winfo_y()

    width_limit = app.winfo_x() + app.winfo_width()
    height_limit = app.winfo_y() + app.winfo_height()

    if event.x_root > width_limit - 120:
        x = app.winfo_width() - 120
    if event.y_root > height_limit - 80:
        y = app.winfo_height() - 80

    def Animation():
        global context_menu_height
        context_menu.configure(height=context_menu_height)
        context_menu.place(x=x, y=y + (30 - context_menu_height/2))

        if context_menu_height < 68:
            context_menu_height += 5
            app.after(10, Animation)
        else:
            context_menu_height = 0

    Animation()

    # Nút Chỉnh sửa
    edit_button = CTkButton(
        master=context_menu,
        text="Chỉnh sửa",
        command=lambda: [EditDataWindow(data), context_menu.destroy()],
        fg_color="transparent",
        hover_color=grey_,
        text_color=text_color,
        corner_radius=8,
        width=100
    )
    edit_button.place(x=10, y=5)

    # Nút Xóa
    delete_button = CTkButton(
        master=context_menu,
        text="Xóa",
        command=lambda: [DeleteDataWindow(data), context_menu.destroy()],
        fg_color="transparent",
        hover_color=grey_,
        text_color=text_color,
        corner_radius=8,
        width=100
    )
    delete_button.place(x=10, y=35)

    # Hàm đóng menu
    def CloseContextMenu(event):
        global context_menu
        if context_menu is not None:
            context_menu.destroy()
            context_menu = None
    app.bind("<Button-1>", CloseContextMenu)


def AddDataWindow() -> None:
    global add_window
    
    gender_=StringVar()
    gender_.set("Nam")

    if add_window and add_window.winfo_exists():
        add_window.focus()
        return

    add_window = CTkToplevel(app, fg_color=grey_)
    add_window.title("Thêm dữ liệu")
    add_window.geometry("700x310+660+400")
    add_window.maxsize(700, 310)
    add_window.minsize(700, 310)
    add_window.grab_set()

    def AddData():
        data = {
            "mssv": mssv_entry.get(),
            "hodem": hodem_entry.get(),
            "name": name_entry.get(),
            "gender": gender_display[gender_.get()],
            "class": class_entry.get(),
            "birth": birth_entry.get(),
            "email": email_entry.get(),
            "owned_cert": owned_cert_entry.get(),
            "tuition": tuition_entry.get(),
            "payed": payed_entry.get(),
            "note": note_entry.get(),
        }


        # Check if any field (except `debt`) is empty
        if not all(data[key] for key in data if key not in ["debt","note"]):
            error_label.configure(text="Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Check for 
        tuition: str = data["tuition"]
        payed: str = data["payed"]
        name: str = data["name"]
        second_name: str = data["hodem"]
        email: str = data["email"]
        owned_cert: str = data["owned_cert"]
        id: str = data["mssv"]

        error_text = ValueValidality(id, name, second_name, email, owned_cert, tuition, payed)

        if error_text != "":
            error_label.configure(text=error_text)
            error_text = ""
            return
         
        # Add the calculated `debt` to the data dictionary
        data["debt"] = int(data["tuition"]) - int(data["payed"])

        DataCorrector(data)

        try:
            collection.insert_one(data)  # Add data to MongoDB
            Log(_id=data["_id"], msg="Thêm sinh viên mới", type="data_change", new_data=data) # Write Log
            add_window.destroy()

            Notificate("Dữ liệu đã được thêm ✅") #Show notificate box

        except Exception as e:
            Log(_id=data["_id"], msg=e, type="error")
            error_label.configure(text=f"Lỗi: {e}")

    def CreateEntry(label_text, row, column):
        label = CTkLabel(master=add_window, text=label_text, text_color=text_color)
        label.grid(row=row, column=column, padx=(20, 5), pady=5)
        entry = CTkEntry(master=add_window, width=200)
        entry.grid(row=row, column=column + 1, padx=5, pady=5)
        return entry

    mssv_entry = CreateEntry("MSSV:", 0, 0)
    hodem_entry = CreateEntry("Họ đệm:", 1, 0)
    name_entry = CreateEntry("Tên:", 2, 0)
    class_entry = CreateEntry("Lớp:", 4, 0)
    birth_entry = CreateEntry("Ngày sinh:", 5, 0)
    email_entry = CreateEntry("Email:", 0, 2)
    owned_cert_entry = CreateEntry("Số TC đã có:", 1, 2)
    tuition_entry = CreateEntry("Tổng học phí:", 2, 2)
    payed_entry = CreateEntry("Học phí đã đóng:", 3, 2)
    note_entry = CreateEntry("Ghi chú:", 4, 2)

    gender_display = {
        "Nam": "Nam",
        "Nữ": "Nữ"
    }

    label = CTkLabel(master=add_window,text="Giới tính:")
    label.grid(row=3,column=0, pady = 5, padx = 5)

    gender_combobox = CTkComboBox(master=add_window, values=list(gender_display.keys()), variable=gender_,width=200)
    gender_combobox.grid(row=3,column=1)


    add_button = CTkButton(master=add_window, text="Thêm", command=AddData)
    add_button.grid(row=11, column=1, padx=20, pady=10)

    cancel_button = CTkButton(master=add_window, text="Xong", command=add_window.destroy)
    cancel_button.grid(row=11, column=3, padx=5, pady=10)

    error_label = CTkLabel(master=add_window, text="", text_color=red_)
    error_label.grid(row=12, column=1, padx=0, pady=0)

# Hàm mở cửa sổ chỉnh sửa dữ liệu
def EditDataWindow(data) -> None:
    global edit_window
    
    gender_=StringVar()
    gender_.set(data["gender"])

    if edit_window and edit_window.winfo_exists():
        edit_window.focus()
        return

    edit_window = CTkToplevel(app, fg_color=grey_)
    edit_window.title("Chỉnh sửa dữ liệu")
    edit_window.geometry("700x310+660+400")
    edit_window.maxsize(700, 310)
    edit_window.minsize(700, 310)
    edit_window.grab_set()

    def UpdateData():
        updated_data = {
            "mssv": mssv_entry.get(),
            "hodem": hodem_entry.get(),
            "name": name_entry.get(),
            "gender": gender_display[gender_.get()],
            "class": class_entry.get(),
            "birth": birth_entry.get(),
            "email": email_entry.get(),
            "owned_cert": owned_cert_entry.get(),
            "tuition": tuition_entry.get(),
            "payed": payed_entry.get(),
            "note": note_entry.get(),
        }

    
        # Check if any field (except `debt`) is empty
        if not all(updated_data[key] for key in updated_data if key not in ["debt","note"]):
            error_label.configure(text="Vui lòng nhập đầy đủ thông tin!")
            return

        tuition = updated_data["tuition"]
        payed = updated_data["payed"]
        name = updated_data["name"]
        second_name = updated_data["hodem"]
        email: str = updated_data["email"]
        owned_cert: str = updated_data["owned_cert"]
        id = updated_data["mssv"]
        _id = data["_id"]

        error_text = ValueValidality(id, name, second_name, email, owned_cert, tuition, payed, _id)

        if error_text != "":
            error_label.configure(text=error_text)
            error_text = ""
            return

        # Add the calculated `debt` to the updated_data dictionary
        updated_data["debt"] = int(updated_data["tuition"]) - int(updated_data["payed"])
        DataCorrector(updated_data)

        old_data = CopyDataFieldNo_ID(data)

        if old_data != updated_data:
            try:
                collection.update_one({"_id": data["_id"]}, {"$set": updated_data})
                Log(_id=data["_id"], msg="Cập nhật dữ liệu sinh viên", type="data_change", new_data=updated_data, old_data=old_data)
                
                document = list(collection.find())
                RefreshTable(document)

                app.after(500, lambda: Notificate("Dữ liệu đã được cập nhật ✅"))
                edit_window.destroy()

            except Exception as e:
                Log(_id=data["_id"], msg=e, type="error")

    def CreateEntry(label_text, initial_value, row, column):
        label = CTkLabel(master=edit_window, text=label_text, text_color=text_color)
        label.grid(row=row, column=column, padx=(20, 5), pady=5)
        entry = CTkEntry(master=edit_window, width=200)
        entry.insert(0, initial_value)
        entry.grid(row=row, column=column + 1, padx=5, pady=5)
        return entry
    
    gender_display = {
        "Nam": "Nam",
        "Nữ": "Nữ"
    }

    # Lấy dữ liệu người dùng
    mssv_entry = CreateEntry("MSSV:", data.get("mssv", ""), 0, 0)
    hodem_entry = CreateEntry("Họ đệm:", data.get("hodem", ""), 1, 0)
    name_entry = CreateEntry("Tên:", data.get("name", ""), 2, 0)
    class_entry = CreateEntry("Lớp:", data.get("class", ""), 4, 0)
    birth_entry = CreateEntry("Ngày sinh:", data.get("birth", ""), 5, 0)
    email_entry = CreateEntry("Email:", data.get("email", ""), 0, 2)
    owned_cert_entry = CreateEntry("Số TC đã có:", data.get("owned_cert", ""), 1, 2)
    tuition_entry = CreateEntry("Tổng học phí:", data.get("tuition", ""), 2, 2)
    payed_entry = CreateEntry("Học phí đã đóng:", data.get("payed", ""), 3, 2)
    note_entry = CreateEntry("Ghi chú:", data.get("note", ""), 4, 2)

    label = CTkLabel(master=edit_window,text="Giới tính:")
    label.grid(row=3,column=0, pady = 5, padx = 5)

    gender_combobox = CTkComboBox(master=edit_window, values=list(gender_display.keys()), variable=gender_, width=200)
    gender_combobox.grid(row=3,column=1)

    # Nút chức năng
    update_button = CTkButton(master=edit_window, text="Cập nhật", command=UpdateData)
    update_button.grid(row=11, column=1, padx=20, pady=10)

    cancel_button = CTkButton(master=edit_window, text="Xong", command=edit_window.destroy)
    cancel_button.grid(row=11, column=3, padx=5, pady=10)

    error_label = CTkLabel(master=edit_window, text="", text_color=red_)
    error_label.grid(row=12, column=1, columnspan=2)

def DeleteDataWindow(data) -> None:
    global delete_window
    # Kiểm tra nếu cửa sổ con đã mở thì không tạo thêm
    if delete_window and delete_window.winfo_exists():
        delete_window.focus()
        return

    delete_window = CTkToplevel(app, fg_color=grey_)
    delete_window.title("Xóa dữ liệu")
    delete_window.geometry("400x100+660+400")
    delete_window.attributes('-topmost', True)

    old_data = CopyDataFieldNo_ID(data)
    def DeleteData():
        Log(_id=data["_id"], msg="Xóa dữ liệu", type="data_change", old_data=old_data)
        collection.delete_one(data)
        delete_window.destroy()

        Notificate("Xóa dữ liệu thành công ✅")

    label = CTkLabel(master=delete_window,text= "Bạn có chắc chắn muốn xóa người này?", anchor="center", text_color=text_color)
    label.grid(row=1,column=0, pady = 5, padx = 10)

    confirm_button = CTkButton(master=delete_window, text="OK", command=DeleteData)
    confirm_button.grid(row=2, column=0, padx=10, pady=10, sticky="e") 

    cancel_button = CTkButton(master=delete_window, text="Hủy", command=delete_window.destroy)
    cancel_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

def SortDataWindow() -> None:
    global sort_window
    if sort_window and sort_window.winfo_exists():
        sort_window.focus()
        return
    
    sort_window = CTkToplevel(app, fg_color=grey_)
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
    label = CTkLabel(master=sort_window,text="Chọn thuộc tính cần sắp xếp", text_color=text_color)
    label.grid(row=1,column=0, pady = 5, padx = 10)
    sort_column_combobox = CTkComboBox(master=sort_window, values=list(display_value.keys()), variable=sort_column, text_color=text_color)
    sort_column_combobox.grid(row=2,column=0, pady = 5, padx = 10)

    sort_option_combobox = CTkComboBox(master=sort_window, values=list(sort_option_display.keys()), variable=sort_option, text_color=text_color)
    sort_option_combobox.grid(row=2,column=1, pady = 5, padx = 10)

    def sort_database() -> None:
        document = collection.find().sort({display_value[sort_column.get()]: sort_option_display[sort_option.get()]})
        RefreshTable(document)
        sort_window.destroy()

    confirm_button = CTkButton(master=sort_window, text="OK", command=sort_database)
    confirm_button.grid(row=3, column=0, padx=10, pady=10, sticky="e") 

    cancel_button = CTkButton(master=sort_window, text="Hủy", command=sort_window.destroy)
    cancel_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

search_result=[]
debounce_id = None
def SearchDataWindow() -> None:
    global search_window
    if search_window and search_window.winfo_exists():
        search_window.focus()
        return

    # Tạo cửa sổ tìm kiếm
    search_window = CTkToplevel(app, fg_color=grey_)
    search_window.title("Tìm kiếm")
    search_window.geometry("550x130+660+400")
    search_window.attributes('-topmost', True)

    # Label và Entry cho từ khóa
    label = CTkLabel(master=search_window, text="Nhập từ khóa cần tìm:", text_color=text_color)
    label.grid(row=0, column=0, pady=5, padx=10)

    entry = CTkEntry(master=search_window, width=240)
    entry.grid(row=1, column=0, pady=5, padx=(20, 5))

    # Các checkbox tùy chọn tìm kiếm
    match_case = BooleanVar()
    match_case_check = CTkCheckBox(master=search_window, text="Match Case", variable=match_case, text_color=text_color)
    match_case_check.grid(row=1, column=1, pady=5, padx=(20, 5))

    match_whole_word = BooleanVar()
    match_whole_word_check = CTkCheckBox(master=search_window, text="Match Whole Word", variable=match_whole_word, text_color=text_color)
    match_whole_word_check.grid(row=1, column=2, pady=5, padx=5)

    # Tạo chỉ mục văn bản toàn bộ (chỉ cần làm một lần duy nhất)
    collection.create_index([("$**", "text")])

    # Hàm tìm kiếm dữ liệu

    def SearchData(event=None) -> None:
        search_data = Search(entry, match_case, match_whole_word)
        pipeline, temp, fields = search_data[0], search_data[1], search_data[2]

        documents = list(collection.aggregate(pipeline))

        global search_result
        search_result = []
        if len(temp) != 0:
            for doc in documents:
                ftemp = []
                for field in fields:
                    value = str(doc.get(field, ""))
                    if temp.lower() in value.lower():
                        ftemp.append(field)
                search_result.append(ftemp)
        RefreshTable(documents)
    def SearchDataDebounced(event=None):
        global debounce_id
        if debounce_id is not None:
            app.after_cancel(debounce_id)
        debounce_id = app.after(400, SearchData)


    # Gắn sự kiện tìm kiếm khi người dùng gõ vào ô nhập
    entry.bind("<KeyRelease>", SearchDataDebounced)

    # Gắn sự kiện để tìm kiếm khi thay đổi giá trị checkbox
    def UpdateSearch():
        SearchData()

    def ResetSearchResult():
        global search_result
        search_result = []
        
    # Khi thay đổi giá trị của checkbox
    match_case_check.configure(command=UpdateSearch)
    match_whole_word_check.configure(command=UpdateSearch)

    search_window.protocol('WM_DELETE_WINDOW', lambda: (ResetSearchResult(), RefreshTable(), search_window.destroy()))
buttons_data = [
    {"image_path": r"template/add_student.png", "command": AddDataWindow, "x": 20, "size": (20, 20)}, 
    {"image_path": r"template/sort.png", "command": SortDataWindow, "x": 75, "size": (20, 20)},
    {"image_path": r"template/search.png", "command": SearchDataWindow, "x": 130, "size": (20, 20)},
    {"image_path": r"template/refresh.png", "command": lambda: RefreshTable(documents=list(collection.find())), "x": 185, "size": (20, 20)},
] # Độ phân giải của ảnh là 512x512 

for button in buttons_data:
    image = PhotoImage(file=button["image_path"]).subsample(*button["size"])
    CTkButton(
        master=app,
        text="",
        image=image,
        command=button["command"],
        width=50,
        height=50,
        fg_color="transparent",
        hover_color=grey_,
    ).place(x=button["x"], y=18)

# Hiển thị tiêu đề và dữ liệu ban đầu
PrintTitle()
RefreshTable()

app.mainloop()
