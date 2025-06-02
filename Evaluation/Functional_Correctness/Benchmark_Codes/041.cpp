#include <iostream>
using namespace std;

class Person {
public:
    string name;

    Person(string n) : name(n) {}

    void greet() {
        cout << "Hello, " + name << endl;
    }
};

int main() {
    Person p("Alice");
    p.greet();
    return 0;
}
