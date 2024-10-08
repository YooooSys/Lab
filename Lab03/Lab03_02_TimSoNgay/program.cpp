#include<iostream>
#include<conio.h>

using namespace std;

//Khai báo nguyên mẫu 
int TimSoNgay(int thang, int nam);
int NhapSoTrongMien(int min, int max);

//Hàm main
int main() {

    int ngay, thang, nam;

    cout << "Nhap mot thang trong nam: ";
    thang = NhapSoTrongMien(1, 12);

    cout << "Nhap nam duong lich";
    nam = NhapSoTrongMien(1, 3000);

    ngay = TimSoNgay(thang, nam);

    cout << endl << "Thang " << thang << " nam " << nam << " co " << ngay << " ngay";

    _getch();
    return 1;
}

//
int NhapSoTrongMien(int min, int max) {
    int so;

    do {
        cout << endl << "Nhap mot so trong doan [" << min << "," << max << "]: ";
        cin >> so;
    } while (so < min || so > max);

    return so; 
}

int TimSoNgay(int thang, int nam) {
    int soNgay;

    if (thang == 4 || thang == 6 || thang == 9 || thang == 11) {
        soNgay == 30;
    }

    else if (thang == 2) {

        if ((nam % 4 == 0 && nam % 100 != 0) || (nam % 400 == 0)) {
                soNgay = 29;
        }
            else {
                soNgay = 28;
            }
    }

    else {
        soNgay = 31;
    }

    return soNgay;
}
//     switch (thang) {
//         case 4:
//         case 6:
//         case 9:
//         case 11:
//             soNgay = 30;
//             break;
            
//         case 2:
//             if ((nam % 4 == 0 && nam % 100 != 0) || (nam % 400 == 0)) {
//                 soNgay = 29;
//             }
//             else {
//                 soNgay = 28;
//             }
//             break;

//         default:
//             soNgay = 31;
//             break;
//     }

//     return soNgay;
// }