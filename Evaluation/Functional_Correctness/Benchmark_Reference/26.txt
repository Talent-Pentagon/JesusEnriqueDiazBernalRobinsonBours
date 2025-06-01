#include <iostream>
using namespace std;

class Counter {
public:
    static int count;
};

int Counter::count = 10;

int main() {
    Counter c;
    cout << c.count << endl;
}
