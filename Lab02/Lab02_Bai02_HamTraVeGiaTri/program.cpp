#include<iostream>
#include<conio.h>

using namespace std;

int NhapSoNguyen();
int TinhTong(unsigned int n);

int main() {
    
    int x, y, z;

    x = NhapSoNguyen();
    y = NhapSoNguyen();

    cout << "Tong hai so la: " << x + y;
    z = (x + y) * NhapSoNguyen();
    cout << endl << "z = " << z;

    int ketQua = 0;
    ketQua = TinhTong(50);
    cout << endl << "1 + 2 + ... + 50 = " << ketQua;

    unsigned int m;
    cout << endl << "Nhap mot so nguyen khong am: ";
    cin >> m;

    ketQua = TinhTong(m);
    cout << endl << "1 + 2 + ... + "<< m << " = " << ketQua;

    return 0;
}

int NhapSoNguyen() {
    int so;

    cout << endl << "Nhap mot so nguyen: ";

    cin >> so;

    return so;
}

int TinhTong(unsigned int n) {
    int sum = 0;

    sum = n * (n + 1) / 2;

    return sum;
}