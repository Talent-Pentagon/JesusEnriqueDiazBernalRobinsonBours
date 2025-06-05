#include <stdio.h>

typedef struct {
    double distance;
    double time;
    double (*speed)(struct Motion*);
} Motion;

double getSpeed(Motion* m) {
    return m->time != 0 ? m->distance / m->time : 0;
}

int main() {
    double distance, time;
    if (scanf("%lf %lf", &distance, &time) != 2) {
        printf("Invalid input\n");
        return 1;
    }
    Motion m = {distance, time, getSpeed};
    printf("Speed: %.2f km/h\n", m.speed(&m));
    return 0;
}
