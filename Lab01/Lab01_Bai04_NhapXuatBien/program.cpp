#include<iostream>

using namespace std;


int main() {
    using namespace std;
    #define MAX 100
    #define KHOA "Cong nghe thong tin"
    #define PI 3.1415926
    #define TAB '\t'
    
    int x = 10, y = 6, z = 9;
    
    cout << "x= " << x << endl;
    cout << "y= " << y << endl;
    cout << "z= " << z ;

    cout << endl
        << x << " + "
        << y << " + "
        << z << " = "
        << x + y + z;

    int dai, rong;

    cout << endl << "Nhap chieu dai cua HCN : ";
    cin >> dai;
    cout << endl << "Nhap chieu rong cua HCN : ";
    cin >> rong;
    cout << endl
        << "Chieu dai hinh chu nhat la " << dai << ", "
        << "chieu rong hinh chu nhat la " << rong;

    int chuVi, dienTich;

    chuVi = (dai + rong) * 2;
    dienTich = dai * rong;

    cout << endl << "Chu vi cua HCM la : " << chuVi;
    cout << endl << "Dien tich cua HCN : " << dienTich;;

    return 0;
}