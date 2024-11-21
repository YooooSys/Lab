from pymongo import MongoClient
import certifi

def get_collection(database_name, collection_name):
    connection_string = "mongodb+srv://giahuy11095:123123123@hyper.kxke3.mongodb.net/"
    client = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = client[database_name]  # Truy cập database
    collection = db[collection_name]  # Truy cập collection
    return collection

def check_student_id(collection, para: dict, _id) -> bool:
    
    students = collection.find(para, {"_id": 1})
    for student in students:
        if _id == None:
            return False
        
        elif student["_id"] != _id:
            return False
        
    return True

def CheckValidValue(id: str, name: str, second_name: str, tuition: str, payed: str, _id=None) -> str:
    
    MAX_NAME = 7
    MAX_SECOND_NAME = 20

    if id.isnumeric() != True:
        return "MSSV không hợp lệ!"
    
    if not check_student_id(collection, {"mssv": id}, _id):
        return "MSSV đã tồn tại!"

    if len(name) > MAX_NAME:
        return "Tên không được dài quá 7 ký tự!"
    
    if len(second_name) > MAX_SECOND_NAME:
        return "Họ đệm không được dài quá 20 kí tự!"
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


collection = get_collection("test_db", "test_collection")