#include <stdio.h>

typedef struct Temperature {
    double celsius;
    double (*toFahrenheit)(struct Temperature*);
} Temperature;

double toFahrenheit(Temperature* temp) {
    return temp->celsius * 9.0 / 5 + 32;
}

int main() {
    double celsius;
    scanf("%lf", &celsius);
    Temperature temp = {celsius, toFahrenheit};
    printf("%.2f\n", temp.toFahrenheit(&temp));
    return 0;
}

