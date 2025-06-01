#include <iostream>
using namespace std;

class Base {
    virtual void show();
};

class Derived : public Base {
public:
    void show() override { 
        cout << "Derived" << endl;
    }
};

int main() {
    Derived d;
    d.show();
}
