from pymongo import MongoClient
import certifi
import re
def get_collection(database_name, collection_name):
    connection_string = "mongodb+srv://giahuy11095:123123123@hyper.kxke3.mongodb.net/"
    client = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = client[database_name]  # Truy cập database
    collection = db[collection_name]  # Truy cập collection
    return collection

def CheckValidStudentId(collection, para: dict, _id) -> bool:
    
    students = collection.find(para)

    for student in students:
        if _id == None:
            return False
        
        elif student["_id"] != _id:
            return False
        
    return True

def CheckValidValue(id: str, name: str, second_name: str, email: str, tuition: str, payed: str, _id=None) -> str:
    
    MAX_NAME: int = 7
    MAX_SECOND_NAME: int = 20
    SPECIAL_CHAR: str = r"-+={}@_!#$%^&*()<>?/\|$}{~:[] "
    
    if id.isnumeric() != True or int(id) < 0 or len(id) != 7:
        return "MSSV không hợp lệ!"

    if not CheckValidStudentId(collection, {"mssv": id}, _id):
        return "MSSV đã tồn tại!"

    if len(name) > MAX_NAME:
        return "Tên không được dài quá 7 ký tự!"
    
    if len(second_name) > MAX_SECOND_NAME:
        return "Họ đệm không được dài quá 20 kí tự!"
    
    for char in name:
        if char in SPECIAL_CHAR:
            return "Tên không hợp lệ"
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return "Email không hợp lệ"
    
    try:
    # Convert the values to integers
        tuition = int(tuition)  # Tổng học phí
        payed = int(payed)  # Học phí đã đóng
        debt = tuition - payed  # Calculate debt
        if debt < 0:
            return "Tổng học phí không thể bé hơn học phí đã đóng!"
        
    except ValueError:
        return "Tổng học phí và học phí đã đóng phải là số!"
    
    return ""

def DataCorrector(data):
    data["mssv"] = int(data["mssv"])
    name = data["name"]
    hodem = data["hodem"]
    data["name"] = name[0].upper() + name[1:].lower()

    data["hodem"] = " ".join(x.title() for x in hodem.split())

collection = get_collection("test_db", "test_collection")