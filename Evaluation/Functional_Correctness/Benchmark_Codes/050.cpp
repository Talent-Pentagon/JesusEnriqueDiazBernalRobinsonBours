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
    string type;
    cin >> type;

    Parent* p = nullptr;

    if (type == "parent")
        p = new Parent();
    else if (type == "child")
        p = new Child();
    else {
        cout << "Unknown type" << endl;
        return 0;
    }

    p->greet();
    delete p;
}
