#include <iostream>
#include <string>
#include <memory>

using namespace std;

class Shape {
public:
    virtual double area() = 0;
    virtual ~Shape() {}
};

class Rectangle : public Shape {
    double width, height;
public:
    Rectangle(double w, double h) : width(w), height(h) {}
    double area() override {
        return width * height;
    }
};

class Circle : public Shape {
    double radius;
public:
    Circle(double r) : radius(r) {}
    double area() override {
        return 3.14159 * radius * radius;
    }
};

int main() {
    string command;
    while (cin >> command) {
        if (command == "rectangle") {
            double w, h;
            cin >> w >> h;
            unique_ptr<Shape> rect = make_unique<Rectangle>(w, h);
            cout << "Rectangle area: " << rect->area() << endl;
        } else if (command == "circle") {
            double r;
            cin >> r;
            unique_ptr<Shape> circ = make_unique<Circle>(r);
            cout << "Circle area: " << circ->area() << endl;
        } else if (command == "exit") {
            break;
        }
    }
    return 0;
}
