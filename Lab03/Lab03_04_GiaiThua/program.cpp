#include <iostream>
#include <conio.h>

using namespace std;

int TinhGiaiThua(unsigned int);
int TinhTong(unsigned int);

int main(int argc, const char **argv) {

	unsigned int n = 0;

	cout << endl << "Nhap mot so nguyen khong am >> "; 
	cin >> n;

	long ketQua = 0;

	ketQua = TinhGiaiThua(n);

	cout << endl << n << "! = " << ketQua;

	ketQua = TinhTong(n);

	cout << endl << "1 + 2 + ... + " << n << " = " << ketQua;

	_getch();
	return 0;
}


int TinhGiaiThua(unsigned int n) {
	int kq = 0;
	if (n < 2) {
		kq = 1;
	}
	else {
		kq = 1; // Khai báo biến lưu kết quả

		for (int i = 2; i <= n; i++) {
			kq *= i;
		}
	}

	return kq;
}


int TinhTong(unsigned int n) {
	int sum = 0; // Khai báo biến để lưu kết quả

	for (int i = 1; i <= n; i++) {
		sum += i;
	}

	return sum;
}
