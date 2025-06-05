#include <iostream>
#include <cstdlib>
using namespace std;

class Animal {
public:
    Animal(int age) { cout << "Animal age: " << age << endl; }
};

class Dog : public Animal {
public:
    Dog(int a) : Animal(a) {}
};

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <age>" << endl;
        return 1;
    }
    int age = atoi(argv[1]);
    Dog d(age);
    return 0;
}
