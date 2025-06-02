#include <stdio.h>
#include <string.h>

typedef struct {
    char name[30];
    int baseSalary;
    int years;
    int (*getBonus)(struct Employee*);
} Employee;

int bonus(Employee* e) {
    return e->baseSalary + (e->years * 1000);
}

int main() {
    Employee e;
    scanf("%s %d %d", e.name, &e.baseSalary, &e.years);
    e.getBonus = bonus;

    printf("Total Salary with Bonus: %d\n", e.getBonus(&e));
    return 0;
}
