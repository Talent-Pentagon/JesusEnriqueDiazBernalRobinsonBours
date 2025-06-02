#include <iostream>
using namespace std;

class Leak {
public:
    Leak() { cout << "Allocated" << endl; }
    ~Leak() { cout << "Deallocated" << endl; }
};

int main() {
    Leak* l = new Leak();
    delete l;
}
