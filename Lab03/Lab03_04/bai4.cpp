#include <iostream>
#include <math.h>

using namespace std;

void XuatSo(unsigned int n); //a
int DemSo(int n);  //b
int DemChuSo(int n);  //c
int DaoSo(int n);  //d
int TongChuSo(int n);   //e
int SoDauTien(int n);   //f
void CoSo2(int n);  //g
int SoHoanHao(int n);   //h
void DemSoHoanHao(int n);   //i
int TimM(int n);    //j

int main()
{
    int n;
    cout << "Nhap n: ";
    cin >> n;
    XuatSo(n);
    cout << endl << "So luong cac so chia het cho 3 nhung khong chia het cho 4 trong khoang [1..." << n << "] la " << DemChuSo(n);
    cout << endl << n << " co " << DemChuSo(n) << " chu so";
    cout << endl << "So dao nguoc cua " << n << " la " << DaoSo(n);
    cout << endl << "Tong chu so trong " << n << " la " << TongChuSo(n);
    cout << endl << "Chu so dau tien cua " << n << " la " << SoDauTien(n)<< endl ;
    CoSo2(n);
    cout << endl;
    if (SoHoanHao(n))
    {
        cout << n << " la so hoan hao" << endl;
    }
    else
    {
        cout << n << " khong la so hoan hao" << endl;
    }
    DemSoHoanHao(n);
    cout << TimM(n) << " la so lon nhat de 1+2+....+" << TimM(n) << " <= " << n;
    return 0;
}

void XuatSo(unsigned int n)
{
    int count = 0;
    for(int i = 1; i <=n ; i++)
    {
        if (count == 10)
        {
            cout << endl;
        }
        cout << i << "\t";
        count++;
    }
}

int DemSo(int n)
{
    int count = 0;
    for(int i = 1; i <= n; i++)
    {
        if (i % 3 == 0 && i % 4 != 0)
        {
            count++;
        }
    }
    return count;
}

int DemChuSo(int n)
{
    int count = 0, data = n;
    while(data > 0)
    {
        count++;
        data /= 10;
    }
    return count;
}

int DaoSo(int n)
{
    int temp, res = 0;
    while(n > 0)
    {
        temp = n % 10;
        res = res * 10 + temp;
        n /= 10;
    }
    return res;
}

int TongChuSo(int n)
{
    int temp, total = 0;
    while(n > 0)
    {
        temp = n % 10;
        total += temp;
        n /= 10;
    }
    return total;
}

int SoDauTien(int n)
{
    int temp, res;
    while(n > 0)
    {
        temp = n % 10;
        res = temp;
        n/=10;
    }
    return res;
}

void CoSo2(int n)
{
    int binary[32];

    int i = 0;
    while (n > 0) {
        binary[i] = n % 2;
        n = n / 2;
        i++;
    }

    for (int j = i - 1; j >= 0; j--)
        cout << binary[j];
}

int SoHoanHao(int n)
{
    int total = 0;
    for(int i = 1; i <= n; i++)
    {
        if(n % i == 0)
        {
            total += i;
        }
    }
    if (total == n * 2)
    {
        return 1;
    }
    return 0;
}

void DemSoHoanHao(int n)
{
    for(int i = 6; i <= n; i++)
    {
        if (SoHoanHao(i))
        {
            cout << i << " la so hoan hao" << endl;
        }
    }
}

int TimM(int n)
{
    int m = 0,i = 1;
    while(m <= n)
    {
        m += i;
        i++;
    }
    return i;
}


