#include <iostream>
using namespace std;

class Person {
    string name;
public:
    Person(string n) {
        name = n;
    }
    void sayName() {
        cout << "Name is: " << name << endl;
    }
};

int main() {
    Person p("Alice");
    p.sayName();
}
