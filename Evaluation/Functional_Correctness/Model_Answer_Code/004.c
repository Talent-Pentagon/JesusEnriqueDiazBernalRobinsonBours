#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int x;
    void (*print)(void);
} Object;

void printObject(Object *obj) {
    printf("x = %d\n", obj->x);
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    int value = atoi(argv[1]);
    Object obj = {value, printObject};
    obj.print();
    return 0;
}