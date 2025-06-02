#include <iostream>
using namespace std;

class Number {
public:
    int get() { return 42; }
};

void display(number n) { 
    cout << "Value: " << n << endl;
}

int main() {
    Number n;
    display(n);
}
