#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct BankAccount {
    int accountNumber;
    double balance;
    void (*deposit)(struct BankAccount*, double);
    void (*withdraw)(struct BankAccount*, double);
    void (*print)(struct BankAccount*);
} BankAccount;

void deposit(BankAccount* acc, double amount) {
    acc->balance += amount;
}

void withdraw(BankAccount* acc, double amount) {
    if (acc->balance >= amount) {
        acc->balance -= amount;
    } else {
        printf("Insufficient funds.\n");
        fflush(stdout);
    }
}

void print(BankAccount* acc) {
    printf("Account #%d, Balance: %.2f\n", acc->accountNumber, acc->balance);
    fflush(stdout);
}

BankAccount createAccount(int accountNumber, double initialBalance) {
    BankAccount acc = {accountNumber, initialBalance, deposit, withdraw, print};
    return acc;
}

int main() {
    BankAccount acc = createAccount(12345, 100.0);
    char command[20];
    double amount;

    while (scanf("%s", command) != EOF) {
        if (strcmp(command, "deposit") == 0) {
            scanf("%lf", &amount);
            acc.deposit(&acc, amount);
        } else if (strcmp(command, "withdraw") == 0) {
            scanf("%lf", &amount);
            acc.withdraw(&acc, amount);
        } else if (strcmp(command, "print") == 0) {
            acc.print(&acc);
        } else if (strcmp(command, "exit") == 0) {
            break;
        }
    }

    return 0;
}
