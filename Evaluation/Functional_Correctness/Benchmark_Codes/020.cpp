#include <iostream>
using namespace std;

class Item {
public:
    ~Item() {
        cout << "Item destroyed" << endl;
    }
};

int main() {
    Item i;
}
