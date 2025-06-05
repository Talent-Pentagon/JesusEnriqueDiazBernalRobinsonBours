#include <iostream>
#include <string>
using namespace std;

class User {
private:
    string username;
    string password;

public:
    User(string user, string pass) {
        username = user;
        password = pass;
    }

    bool authenticate(string inputUser, string inputPass) {
        return (inputUser == username && inputPass == password);
    }

    void changePassword(string oldPass, string newPass) {
        if (oldPass == password) {
            password = newPass;
            cout << "Password changed successfully.\n";
        } else {
            cout << "Incorrect old password.\n";
        }
    }
};

int main() {
    User user("admin", "secure123");

    string inputUser, inputPass;
    cin >> inputUser >> inputPass;  // read username and password

    if (user.authenticate(inputUser, inputPass)) {
        cout << "Login successful!\n";
    } else {
        cout << "Login failed. Invalid credentials.\n";
    }

    return 0;
}
