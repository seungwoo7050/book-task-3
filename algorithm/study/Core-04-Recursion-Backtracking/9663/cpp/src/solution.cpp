#include <bits/stdc++.h>
using namespace std;

int n, cnt = 0;
bool col_used[15], diag1[30], diag2[30];

void place(int row) {
    if (row == n) { cnt++; return; }
    for (int c = 0; c < n; c++) {
        if (!col_used[c] && !diag1[row - c + n - 1] && !diag2[row + c]) {
            col_used[c] = diag1[row - c + n - 1] = diag2[row + c] = true;
            place(row + 1);
            col_used[c] = diag1[row - c + n - 1] = diag2[row + c] = false;
        }
    }
}

int main() {
    cin >> n;
    place(0);
    cout << cnt << '\n';
    return 0;
}
