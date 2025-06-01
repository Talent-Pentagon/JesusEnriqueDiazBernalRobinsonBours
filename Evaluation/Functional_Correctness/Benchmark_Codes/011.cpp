#include <iostream>
using namespace std;

class Rectangle {
private:
    int width, height;
public:
    Rectangle(int w, int h) : width(w), height(h) {}
    int area() { return width * height; }
};

int main() {
    int w, h;
    cin >> w >> h;
    Rectangle rect(w, h);
    cout << rect.area() << endl;
    return 0;
}
