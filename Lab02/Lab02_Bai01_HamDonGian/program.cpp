#include<iostream>
#include<conio.h>
#include<iomanip>

using namespace std;

void XuatPhuongTrinh(float a, float b);
void ThongBao();
void XuatKyTu(short ma);

int main() {

    ThongBao();
    
    XuatKyTu(157);
    
    short dollar = 36, ma;
    XuatKyTu(dollar);

    XuatPhuongTrinh(2.3, 5);

    float p, q = 10;
    XuatPhuongTrinh(7.5, q);

    cout << endl << "Nhap mot so thuc: ";
    cin >> p;

    XuatPhuongTrinh(p, q);

    _getch();

    return 0;
}


void XuatPhuongTrinh(float a, float b) {
    cout << endl << a << "x + " << b << " = 0";
}
void ThongBao() {

    cout << endl << "Ban phai hoan thanh bai tap nay.";

}

void XuatKyTu(short ma) {
    char kyTu = ma;
    cout << endl << ma << " <=> " << kyTu;
}