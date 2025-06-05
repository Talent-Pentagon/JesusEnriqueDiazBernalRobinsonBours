#include <iostream>
using namespace std;

class SelfCopy {
public:
    int value;

    SelfCopy(int v) : value(v) {}

    SelfCopy(const SelfCopy& other) {
        value = other.value;
    }

    void print() {
        cout << "Value: " << value << endl;
    }
};

int main() {
    SelfCopy a(10);
    SelfCopy b = a;
    b.print();
    return 0;
}