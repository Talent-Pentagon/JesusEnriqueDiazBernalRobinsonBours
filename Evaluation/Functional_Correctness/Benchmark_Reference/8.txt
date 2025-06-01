#include <iostream>
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
    Shape* rect = new Rectangle(4.0, 5.0);
    Shape* circ = new Circle(3.0);
    cout << "Rectangle area: " << rect->area() << endl;
    cout << "Circle area: " << circ->area() << endl;
    delete rect;
    delete circ;
    return 0;
}
