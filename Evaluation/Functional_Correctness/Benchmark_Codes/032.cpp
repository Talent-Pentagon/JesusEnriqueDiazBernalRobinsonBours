#include <iostream>
using namespace std;

class Demo {
    int x = 5;
public:
    void show() {
        cout << this->x << endl;
    }
};

int main() {
    Demo d;
    d.show();
}
