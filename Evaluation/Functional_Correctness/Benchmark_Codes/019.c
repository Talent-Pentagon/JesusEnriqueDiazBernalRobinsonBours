#include <stdio.h>

typedef struct {
    double radius;
    double (*circumference)(struct Circle*);
} Circle;

double getCircumference(Circle* c) {
    return 2 * 3.14159 * c->radius;
}

int main() {
    double radius;
    scanf("%lf", &radius);
    Circle c = {radius, getCircumference};
    printf("%.2f\n", c.circumference(&c));
    return 0;
}
