#include <stdio.h>

typedef struct {
    double fahrenheit;
    double (*toCelsius)(struct Temp*);
} Temp;

double convertToCelsius(Temp* t) {
    return (t->fahrenheit - 32) * 5.0 / 9;
}

int main() {
    double fahrenheit;
    scanf("%lf", &fahrenheit);
    Temp temp = {fahrenheit, convertToCelsius};
    printf("%.2f\n", temp.toCelsius(&temp));
    return 0;
}
