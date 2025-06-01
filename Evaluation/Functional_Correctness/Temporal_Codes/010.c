#include <stdio.h>
#include <string.h>

typedef struct Employee {
    char name[50];
    double hoursWorked;
    double hourlyRate;
    double (*calculatePay)(struct Employee*);
} Employee;

double calculatePay(Employee* emp) {
    return emp->hoursWorked * emp->hourlyRate;
}

int main() {
    char name[50];
    double hours, rate;

    while (scanf("%49s %lf %lf", name, &hours, &rate) == 3) {
        Employee emp;
        strncpy(emp.name, name, sizeof(emp.name) - 1);
        emp.name[sizeof(emp.name) - 1] = '\0';
        emp.hoursWorked = hours;
        emp.hourlyRate = rate;
        emp.calculatePay = calculatePay;

        printf("Pay for %s: %.2f\n", emp.name, emp.calculatePay(&emp));
    }
    return 0;
}
