#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        string keys;
        cin >> keys;

        list<char> editor;
        auto cursor = editor.end();

        for (char ch : keys) {
            if (ch == '<') {
                if (cursor != editor.begin()) --cursor;
            } else if (ch == '>') {
                if (cursor != editor.end()) ++cursor;
            } else if (ch == '-') {
                if (cursor != editor.begin()) {
                    auto it = prev(cursor);
                    editor.erase(it);
                }
            } else {
                editor.insert(cursor, ch);
            }
        }

        for (char c : editor) cout << c;
        cout << '\n';
    }

    return 0;
}
