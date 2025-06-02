#include <iostream>
using namespace std;

class Box {
private:
    int length;
    int width;

public:
    Box(int l, int w) : length(l), width(w) {}

    int getArea() {
        return length * width;
    }
};

int main() {
    Box b(4, 5);
    cout << "Area: " << b.getArea() << endl;
    return 0;
}
