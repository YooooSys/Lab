#include <iostream>
#include <conio.h>

using namespace std;

void ThongKe(unsigned int n);
unsigned short NhapDiem(int stt);

int main(int argc, const char **argv) {

	unsigned int n = 0;

	cout << endl << "Nhap so luong sinh vien : ";
	cin >> n;

	ThongKe(n);

	_getch();
	return 0;
}


unsigned short NhapDiem(int stt) {
	unsigned short diem = 0;
	do {
		cout << endl << "Nhap diem cua SV thu " << stt << " : ";
		cin >> diem;
	} while (diem < 0 || diem > 10);
	return diem;
}


void ThongKe(unsigned int n) {
	// Khai báo các biến đếm để thống kê theo điểm số
	int d0 = 0, d1 = 0, d2 = 0, d3 = 0, d4 = 0, d5 = 0,
		d6 = 0, d7 = 0, d8 = 0, d9 = 0, d10 = 0;

	unsigned short diem = 0;

	// Duyệt qua từng sinh viên
	for (int i = 0; i < n; i++) {
		// Nhập điểm cho sinh viên thứ i 
		diem = NhapDiem(i + 1);

		switch (diem) {
			case 10: d10++;
			case 9: d9++;
			case 8: d8++;
			case 7: d7++;
			case 6: d6++;
			case 5: d5++;
			case 4: d4++;
			case 3: d3++;
			case 2: d2++;
			case 1: d1++;
			case 0: d0++;
		}
	}

	// Xuất kết quả thống kê
	cout << endl << "So sinh vien co diem >= 0 : " << d0;
	cout << endl << "So sinh vien co diem >= 1 : " << d1;
	cout << endl << "So sinh vien co diem >= 2 : " << d2;
	cout << endl << "So sinh vien co diem >= 3 : " << d3;
	cout << endl << "So sinh vien co diem >= 4 : " << d4;
	cout << endl << "So sinh vien co diem >= 5 : " << d5;
	cout << endl << "So sinh vien co diem >= 6 : " << d6;
	cout << endl << "So sinh vien co diem >= 7 : " << d7;
	cout << endl << "So sinh vien co diem >= 8 : " << d8;
	cout << endl << "So sinh vien co diem >= 9 : " << d9;
	cout << endl << "So sinh vien co diem = 10 : " << d10;
}
