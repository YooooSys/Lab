from pymongo import MongoClient, ASCENDING
import datetime
import certifi
import re
def get_collection(database_name, collection_name):
    connection_string = "mongodb+srv://giahuy11095:123123123@hyper.kxke3.mongodb.net/"
    client = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = client[database_name]  # Truy cập database
    collection = db[collection_name]  # Truy cập collection
    return collection

def Search(entry, match_case, match_whole_word, mode=1): # Mode 1 will return documents
    temp = entry.get()
    fields = [
        "mssv", "hodem", "name", "gender", 
        "class", "birth", "email", "owned_cert", 
        "tuition", "payed", "debt", "note"
    ]
    
    # Lấy giá trị của các checkbox
    match_case_value = match_case.get()
    match_whole_word_value = match_whole_word.get()

    # Điều kiện tìm kiếm dựa trên các tùy chọn
    if not match_case_value and not match_whole_word_value:
        conditions = {
            "$or": [
                {field: {"$regex": temp, "$options": "i"}} for field in fields
            ]
        }
    elif match_case_value and not match_whole_word_value:
        conditions = {
            "$or": [
                {field: {"$regex": temp}} for field in fields
            ]
        }
    elif not match_case_value and match_whole_word_value:
        # Sử dụng regex để tìm từ đầy đủ
        conditions = {
            "$or": [
                {field: {"$regex": r"\b" + temp + r"\b", "$options": "i"}} for field in fields
            ]
        }
    else:
        conditions = {
            "$or": [
                {field: {"$regex": r"\b" + temp + r"\b"}} for field in fields
            ]
        }

    # Pipeline tìm kiếm
    pipeline = [
        # Chuyển đổi các trường số thành chuỗi
        {
            "$addFields": {
                "mssv": {"$toString": "$mssv"},
                "tuition": {"$toString": "$tuition"},
                "payed": {"$toString": "$payed"},
                "debt": {"$toString": "$debt"},
            }
        },
        # Thực hiện tìm kiếm
        {"$match": conditions},
        # Khôi phục các trường về kiểu số
        {
            "$addFields": {
                "mssv": {"$toInt": "$mssv"},
                "tuition": {"$toInt": "$tuition"},
                "payed": {"$toInt": "$payed"},
                "debt": {"$toInt": "$debt"},
            }
        }
    ]
    
    return [pipeline, temp, fields]
    
def CheckValidStudentId(collection, para: dict, _id) -> bool: # return False when a student with "mssv" value already exist 
    
    students = collection.find(para)

    for student in students:
        if _id == None or student["_id"] != _id:
            return False

    return True

def CopyDataFieldNo_ID(field: dict):
    newfield = {}
    for key, value in field.items():
        if key != "_id":
            newfield[key] = value
    return newfield

def ValueValidality(id: str, name: str, second_name: str, email: str, owned_cert: str, tuition: str, payed: str, _id=None) -> str: 
    
    MAX_NAME: int = 7
    MAX_SECOND_NAME: int = 20
    SPECIAL_CHAR: str = r"-+={}@_!#$%^&*()<>?/\|$}{~:[] 0123456789"
    
    if not(id.isnumeric()) or int(id) < 0 or len(id) != 7:
        return "MSSV không hợp lệ!"

    if not CheckValidStudentId(collection, {"mssv": id}, _id):
        return "MSSV đã tồn tại!"

    if len(name) > MAX_NAME:
        return "Tên không được dài quá 7 ký tự!"
    
    if len(second_name) > MAX_SECOND_NAME:
        return "Họ đệm không được dài quá 20 kí tự!"
    
    for char in second_name:
        if char in SPECIAL_CHAR and char != " ":
            return "Họ đệm không hợp lệ"
        
    for char in name:
        if char in SPECIAL_CHAR:
            return "Tên không hợp lệ"
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return "Email không hợp lệ"
    
    try:
        owned_cert = int(owned_cert)
    except ValueError:
        return "Số tín chỉ không hợp lệ"
    
    try:
        tuition = int(tuition)  # Tổng học phí
        payed = int(payed)  # Học phí đã đóng
        debt = tuition - payed  # Calculate debt
        if debt < 0:
            return "Tổng học phí không thể bé hơn học phí đã đóng!"
        
    except ValueError:
        return "Tổng học phí và học phí đã đóng phải là số!"
    
    return ""

def DataCorrector(data) -> None:
    data["mssv"] = int(data["mssv"])
    name = data["name"]
    hodem = data["hodem"]

    data["name"] = name.title()

    data["hodem"] = " ".join(x.title() for x in hodem.split())

    data["tuition"] = int(data["tuition"])

    data["owned_cert"] = int(data["owned_cert"])
collection = get_collection("test_db", "test_collection")


def Log(_id: object ,msg: str, type: str, new_data: dict={}, old_data: dict={}, auth: str=None):
    entry = {}
    entry['timestamp'] = datetime.datetime.now()
    entry["id"] = _id
    entry['msg'] = msg
    entry["type"] = type

    if type == "data_change":
        entry["new"] = new_data
        entry["old"] = old_data

    entry["auth"] = auth
    log_collection.insert_one(entry)


log_collection = get_collection("test_db", "_log")

