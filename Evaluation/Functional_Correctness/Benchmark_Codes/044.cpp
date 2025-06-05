#include <iostream>
using namespace std;

class Calculator {
public:
    int sum(int a, int b) {
        int result = a + b;
        return result;
    }
};

int main() {
    Calculator c;
    int a, b;
    while (cin >> a >> b) {
        cout << c.sum(a, b) << endl;
    }
    return 0;
}
