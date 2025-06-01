#include <iostream>
using namespace std;

class A {
private:
    int value = 42;
public:
    friend void show(A& a);
};

void show(A& a) {
    cout << a.value << endl;
}

int main() {
    A obj;
    show(obj);
    return 0;
}