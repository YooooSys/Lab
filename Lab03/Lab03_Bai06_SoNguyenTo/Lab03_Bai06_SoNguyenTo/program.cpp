#include <iostream>
#include <conio.h>
#include <cmath>

using namespace std;

#define		TAB		'\t'

void LietKeSoNT(unsigned int n);
int KiemTra_NT(int n);

int main() {

	unsigned int n = 0;

	cout << endl << "Nhap so luong so NT can tim : ";
	cin >> n;

	LietKeSoNT(n);

	_getch();
	return 0;
}

int KiemTra_NT(int n) {
	int kq = 0, m = 0, i = 0;
	if (n < 2) {
		kq = 0;
	}
	else {
		m = (int)sqrt((double)n);
		i = 2;
		kq = 1;

		while (i <= m && kq) {
			if (n % i == 0) {
				kq = 0;
			}
			i++;
		}
	}
	return kq;
}


void LietKeSoNT(unsigned int n) {
	int dem = 0, so = 2;

	while (dem < n) {
		if (KiemTra_NT(so)) {
			cout << so << TAB;
			dem++;
		}

		so++;
	}
}
