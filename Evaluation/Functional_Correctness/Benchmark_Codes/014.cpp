#include <iostream>
using namespace std;

class Animal {
public:
    Animal(int age) { cout << "Animal age: " << age << endl; }
};

class Dog : public Animal {
public:
    Dog(int a) : Animal(a) {}
};

int main() {
    Dog d(5);
}
