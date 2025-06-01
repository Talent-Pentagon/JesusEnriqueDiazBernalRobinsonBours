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
    cout << c.sum(3, 4) << endl;
}
