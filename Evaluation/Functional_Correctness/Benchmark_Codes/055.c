#include <stdio.h>

typedef struct {
    double price;
    double (*getDiscount)(double);
} Order;

double flatDiscount(double price) {
    return price * 0.90;
}

double seasonalDiscount(double price) {
    return price > 100 ? price * 0.85 : price * 0.95;
}

int main() {
    Order o1 = {150.0, flatDiscount};
    Order o2 = {150.0, seasonalDiscount};

    printf("Flat: %.2f\n", o1.getDiscount(o1.price));
    printf("Seasonal: %.2f\n", o2.getDiscount(o2.price));
    return 0;
}