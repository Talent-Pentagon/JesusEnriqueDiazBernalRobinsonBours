#include <iostream>
using namespace std;

class Calculator {
public:
    int add(int a, int b) {
        return a + b;
    }

    int multiply(int a, int b) {
        return a * b;
    }
};

int main() {
    Calculator calc;
    int result = calc.add(3, 4);
    cout << "Result: " << result << endl;
    return 0;
}
