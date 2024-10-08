#include <iostream>
#include <conio.h>
#include<iomanip>
#include<math.h>
using namespace std;
void GiaiPhuongTrinhBacHai( float a, float b, float c);
float NhapMotSoKhacKhong();
int main()
{ 
    float a,b,c;
    a = NhapMotSoKhacKhong();
    cout << endl << " Nhap he so b : ";
    cin >> b;
    cout << endl << " Nhap he so c : ";
    cin >> c;
    GiaiPhuongTrinhBacHai(a, b, c);
    _getch();
    return 1;
}
float NhapMotSoKhacKhong()
{
    float so;
    // sài while sẽ tạo ra bug nên sài do...while sẽ tối ưu và hợp lí hơn
    do
    {
        cout << endl << " nhap mot so thuc (khac 0) : ";
        cin >> so;
    }while (so == 0);
    return so;
}
void GiaiPhuongTrinhBacHai( float a, float b, float c)
{
    double Delta,
        x;
    Delta = b * b - 4 * a * c;
    if (Delta < 0)
    {
        cout << endl << " Phuong trinh vo nghiem";
    }
    else if (Delta == 0.0)
    {   
        x = -b/(2*a);
        cout << endl << " phuong trinh co nghiem kep x = " << x;
    }
    else
    {
        cout << endl << " Phuong trinh co hai nghiem phan biet :";
        x = (-b + sqrt(Delta)) / (2 * a);
        cout << "x1 = " << setprecision(5) << x; //setprecision có tác dụng là chỉ lấy n chữ sau ở sau phần thập phân, trường hợp này là 5
        x = (-b - sqrt(Delta)) / (2 * a);
        cout << "x2 = " << setprecision(5) << x;
    }
}
