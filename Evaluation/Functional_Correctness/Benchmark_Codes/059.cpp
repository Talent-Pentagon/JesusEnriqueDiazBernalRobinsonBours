#include <iostream>
#include <vector>
using namespace std;

class Leak {
public:
    Leak() { cout << "Allocated" << endl; }
    ~Leak() { cout << "Deallocated" << endl; }
};

int main() {
    int n;
    cin >> n;

    vector<Leak*> leaks;

    for (int i = 0; i < n; ++i) {
        leaks.push_back(new Leak());
    }

    for (int i = 0; i < n; ++i) {
        delete leaks[i];
    }

    return 0;
}
