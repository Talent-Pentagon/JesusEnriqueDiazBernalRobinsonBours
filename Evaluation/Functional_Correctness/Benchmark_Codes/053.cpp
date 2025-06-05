#include <iostream>
using namespace std;

class Base {
public:
    virtual void show() {
        cout << "Base" << endl;
    }
};

class Derived : public Base {
public:
    void show() override {
        cout << "Derived" << endl;
    }
};

int main() {
    string type;
    cin >> type;

    Base* b = nullptr;

    if (type == "base") {
        b = new Base();
    } else if (type == "derived") {
        b = new Derived();
    } else {
        cout << "Unknown" << endl;
        return 0;
    }

    b->show();
    delete b;
}
