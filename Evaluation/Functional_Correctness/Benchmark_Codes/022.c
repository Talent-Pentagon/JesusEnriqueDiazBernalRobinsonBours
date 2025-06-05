#include <stdio.h>

typedef struct {
    double principal;
    double rate;
    int time;
    double (*interest)(struct Loan*);
} Loan;

double getInterest(Loan* l) {
    return (l->principal * l->rate * l->time) / 100.0;
}

int main() {
    double principal, rate;
    int time;
    scanf("%lf %lf %d", &principal, &rate, &time);
    Loan loan = {principal, rate, time, getInterest};
    printf("%.2f\n", loan.interest(&loan));
    return 0;
}
