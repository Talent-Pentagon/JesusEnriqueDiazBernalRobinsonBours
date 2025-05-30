#include <iostream>
using namespace std;

class Car {
    string model;
public:
    Car(string m) : model(m) {
        model = m;
    }
    void show() {
        cout << "Model: " << model << endl;
    }
};

int main(int argc, char* argv[]) {
    if (argc < 2) return 1;
    Car c(argv[1]);
    c.show();
    return 0;
}