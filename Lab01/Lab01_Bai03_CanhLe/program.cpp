#include <iostream>
#include <iomanip>
#include <conio.h>

using namespace std;

int main() {
    cout << setiosflags(ios::left)
        << setw(10) << "MSSV"
        << setw(10) << "Ho va ten"
        << setw(25) << "Lop"
        << setw(10) << "Diem TB"
        << setw(10) << "Diem TL"
        << endl;
    
    cout << setiosflags(ios::left)
        << setw(10) << "123412"
        << setw(25) << "Nguyen Quang Tam"
        << setw(10) << "CTK48"
        << setw(10) << "1.0"
        << setw(10) << setprecision(2) << 1.23
        << endl;
    
    cout << setiosflags(ios::left)
        << setw(10) << "12312312"
        << setw(25) << "Nguyen Cong Thai Hoc"
        << setw(10) << "CTK47"
        << setw(10) << "9.0"
        << setw(10) << setprecision(2) << 2.11
        << endl;
    
    cout << setiosflags(ios::left)
        << setw(10) << "158712"
        << setw(25) << "Pham Thi Quang Tam"
        << setw(10) << "CTK46"
        << setw(10) << "2.6"
        << setw(10) << setprecision(2) << 12.23
        << endl;
    
    cout << setiosflags(ios::left)
        << setw(10) << "1231522"
        << setw(25) << "Nguyen Quang Tam"
        << setw(10) << "CTK48"
        << setw(10) << "1.0"
        << setw(10) << setprecision(2) << 1.26
        << endl;
        
    cout << setiosflags(ios::left)
        << setw(10) << "984954"
        << setw(25) << "Nguyen Thi Nghia"
        << setw(10) << "CTK42"
        << setw(10) << "8.0"
        << setw(10) << setprecision(2) << 6.0
        << endl;


    return 0;
}