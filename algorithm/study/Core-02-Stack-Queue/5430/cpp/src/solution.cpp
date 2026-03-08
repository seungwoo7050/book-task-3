#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        string p;
        cin >> p;
        int n;
        cin >> n;
        string arr_str;
        cin >> arr_str;

        deque<string> dq;
        // Parse "[x1,x2,...,xn]"
        string num;
        for (int i = 1; i < (int)arr_str.size(); i++) {
            if (arr_str[i] == ',' || arr_str[i] == ']') {
                if (!num.empty()) {
                    dq.push_back(num);
                    num.clear();
                }
            } else {
                num += arr_str[i];
            }
        }

        bool is_reversed = false;
        bool error = false;

        for (char cmd : p) {
            if (cmd == 'R') {
                is_reversed = !is_reversed;
            } else { // D
                if (dq.empty()) { error = true; break; }
                if (is_reversed) dq.pop_back();
                else dq.pop_front();
            }
        }

        if (error) {
            cout << "error\n";
        } else {
            cout << '[';
            if (is_reversed) {
                for (int i = (int)dq.size() - 1; i >= 0; i--) {
                    if (i < (int)dq.size() - 1) cout << ',';
                    cout << dq[i];
                }
            } else {
                for (int i = 0; i < (int)dq.size(); i++) {
                    if (i) cout << ',';
                    cout << dq[i];
                }
            }
            cout << "]\n";
        }
    }
    return 0;
}
