#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

class Illness {
private:
    string name;
    int severity;

public:
    Illness(const string& name, int severity)
        : name(name), severity(severity) {}

    string getName() const {
        return name;
    }

    int getSeverity() const {
        return severity;
    }

    void print() const {
        cout << "- " << name << " (Severity: " << severity << ")" << endl;
    }

    bool operator==(const Illness& other) const {
        return name == other.name;
    }
};

class Moises {
private:
    string name;
    vector<Illness> illnesses;

public:
    Moises(const string& name) : name(name) {}

    void catchIllness(const Illness& illness) {
        if (find(illnesses.begin(), illnesses.end(), illness) == illnesses.end()) {
            illnesses.push_back(illness);
        }
    }

    void recoverFrom(const string& illnessName) {
        illnesses.erase(
            remove_if(illnesses.begin(), illnesses.end(),
                [&](const Illness& ill) { return ill.getName() == illnessName; }),
            illnesses.end()
        );
    }

    bool isHealthy() const {
        return illnesses.empty();
    }

    void printStatus() const {
        cout << name << " is currently " << (isHealthy() ? "healthy." : "sick with:") << endl;
        for (const auto& illness : illnesses) {
            illness.print();
        }
    }
};

int main() {
    string action, name;
    int severity;
    Moises moises("Moises");

    while (cin >> action) {
        if (action == "catch") {
            cin >> name >> severity;
            moises.catchIllness(Illness(name, severity));
        } else if (action == "recover") {
            cin >> name;
            moises.recoverFrom(name);
        } else if (action == "status") {
            moises.printStatus();
        } else if (action == "exit") {
            break;
        }
    }

    return 0;
}
