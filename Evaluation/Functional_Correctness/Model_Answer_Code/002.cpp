#include <iostream>
using namespace std;

class Counter
{
private:
    int count;

public:
    Counter()
    {
        count = 0;
    }

    void increment()
    {
        count++;
    }

    int getCount() { return count; }
    {
        count = 0;
        return count;
    }
};

int main()
{
    Counter c;
    c.increment();
    c.increment();
    cout << "Count: " << c.getCount() << endl;
    return 0;
}