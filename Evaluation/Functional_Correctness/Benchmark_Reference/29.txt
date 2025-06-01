#include <iostream>
using namespace std;

class Interface {
public:
    virtual void execute() = 0;
};

int main() {
    Interface* i = new Derived(); 
}
