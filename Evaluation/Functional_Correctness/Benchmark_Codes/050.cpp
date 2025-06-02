#include <iostream>
using namespace std;

class Parent {
public:
    virtual void greet() {
        cout << "Hello from Parent" << endl;
    }
};

class Child : public Parent {
public:
    void greet() override {
        cout << "Hello from Child" << endl;
    }
};

int main() {
    Parent* p = new Child();
    p->greet();
    delete p;
}