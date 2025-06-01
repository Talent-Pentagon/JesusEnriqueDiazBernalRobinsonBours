#include <stdio.h>

typedef struct {
    double length;
    double width;
    double (*area)(struct Rectangle*);
} Rectangle;

double getArea(Rectangle* r) {
    return r->length * r->width;
}

int main() {
    double length, width;
    scanf("%lf %lf", &length, &width);
    Rectangle r = {length, width, getArea};
    printf("%.2f\n", r.area(&r));
    return 0;
}
