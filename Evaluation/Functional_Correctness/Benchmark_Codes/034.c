#include <stdio.h>
#include <string.h>

typedef struct Account Account;

struct Account {
    char owner[50];
    double balance;
    void (*deposit)(Account*, double);
    int (*withdraw)(Account*, double);
    void (*print)(Account*);
};

void deposit(Account* acc, double amount) {
    acc->balance += amount;
}

int withdraw(Account* acc, double amount) {
    if (amount <= acc->balance) {
        acc->balance -= amount;
        return 1;
    }
    return 0;
}

void print(Account* acc) {
    printf("Owner: %s | Balance: %.2f\n", acc->owner, acc->balance);
}

int main() {
    Account acc = {"Alice", 1000.0, deposit, withdraw, print};
    int n;
    scanf("%d", &n);  // Number of operations

    for (int i = 0; i < n; i++) {
        char op[50];
        double amount;
        scanf("%s", op);

        if (strcmp(op, "deposit") == 0) {
            scanf("%lf", &amount);
            acc.deposit(&acc, amount);
        } else if (strcmp(op, "withdraw") == 0) {
            scanf("%lf", &amount);
            if (!acc.withdraw(&acc, amount)) {
                printf("Insufficient funds\n");
            }
        } else if (strcmp(op, "print") == 0) {
            acc.print(&acc);
        } else {
            printf("Unknown operation: %s\n", op);
            // Discard rest of the line to avoid reading parameters as next op
            int ch;
            while ((ch = getchar()) != '\n' && ch != EOF);
        }
    }

    return 0;
}
