#include <iostream>
#include <cstdlib>
using namespace std;

class Box {
public:
    int width;
    Box(int w) : width(w) {}
};

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <width>" << endl;
        return 1;
    }
    int width = atoi(argv[1]);
    Box b(width);
    cout << b.width << endl;
    return 0;
}
