#include <iostream>
#include <string>
using namespace std;

class Man {
private:
    string name;
    bool inJail;

public:
    Man(const string& name) : name(name), inJail(false) {}

    void goToJail() {
        inJail = true;
        cout << name << " is now in jail." << endl;
    }

    void release() {
        inJail = false;
        cout << name << " has been released from jail." << endl;
    }

    bool isInJail() const {
        return inJail;
    }

    string getName() const {
        return name;
    }
};

int main() {
    string name, command;
    getline(cin, name);
    Man m(name);
    cout << m.getName() << " starts free." << endl;

    while (getline(cin, command)) {
        if (command == "jail") {
            m.goToJail();
            if (m.isInJail()) {
                cout << m.getName() << " is currently in jail." << endl;
            }
        } else if (command == "release") {
            m.release();
            if (!m.isInJail()) {
                cout << m.getName() << " is no longer in jail." << endl;
            }
        }
    }
    return 0;
}
