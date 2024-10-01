#include<iostream>
#include<conio.h>
#include<math.h>

using namespace std;

int TinhDienTichTamGiac(int a, int b, int c);
int TinhDienTichHCN(int dai, int rong);

int main() {
    int a, b, c;
    double dienTich;

    //Dien tich tam giac
    cout << endl << "Nhap do dai ba canh a, b, c: ";
    cin >> a >> b >> c;

    // Dien tich HCN
    dienTich = TinhDienTichHCN(a, b);
    cout << endl << "Dien tich cua hinh chu nhat co "
        << "chieu dai " << a << " va "
        << "chieu rong " << b << " la "
        << dienTich;

    dienTich = TinhDienTichTamGiac(a, b, c);
    cout << endl << "Dien tich cua hinh tam giac co "
        << "3 canh: a = " << a << ", "
        << "b = " << b << ", c = " << c << " la "
        << dienTich;

    return 0;
}

int TinhDienTichHCN(int dai, int rong) {

    int dienTich;
    dienTich = dai * rong;
    
    return dienTich;
}

int TinhDienTichTamGiac(int a, int b, int c) {
    double dienTich, p;

    p = (a + b + c) / 2;

    dienTich = sqrt(p * (p - a) * (p - b) * (p - c));

    return dienTich;
}