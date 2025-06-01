#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Base "class"
typedef struct Dinosaur {
    char name[50];
    int age;          // in millions of years
    double length;    // in meters

    void (*roar)(struct Dinosaur*); // method pointer
    void (*info)(struct Dinosaur*);
} Dinosaur;

// Base methods
void Dinosaur_roar(Dinosaur* dino) {
    printf("%s roars loudly!\n", dino->name);
}

void Dinosaur_info(Dinosaur* dino) {
    printf("Name: %s\n", dino->name);
    printf("Age: %d million years ago\n", dino->age);
    printf("Length: %.2f meters\n", dino->length);
}

// Derived "class": T-Rex
typedef struct TRex {
    Dinosaur base;  // inherit Dinosaur fields and methods
} TRex;

void TRex_roar(Dinosaur* dino) {
    printf("%s lets out a terrifying roar!\n", dino->name);
}

void TRex_hunt(TRex* trex) {
    printf("%s is hunting its prey.\n", trex->base.name);
}

TRex* TRex_new(int age, double length) {
    TRex* trex = malloc(sizeof(TRex));
    strcpy(trex->base.name, "T-Rex");
    trex->base.age = age;
    trex->base.length = length;

    trex->base.roar = TRex_roar;
    trex->base.info = Dinosaur_info; // reuse base info method

    return trex;
}

// Derived "class": Triceratops
typedef struct Triceratops {
    Dinosaur base;
} Triceratops;

void Triceratops_roar(Dinosaur* dino) {
    printf("%s makes a grunt sound.\n", dino->name);
}

void Triceratops_defend(Triceratops* tri) {
    printf("%s defends itself with its horns.\n", tri->base.name);
}

Triceratops* Triceratops_new(int age, double length) {
    Triceratops* tri = malloc(sizeof(Triceratops));
    strcpy(tri->base.name, "Triceratops");
    tri->base.age = age;
    tri->base.length = length;

    tri->base.roar = Triceratops_roar;
    tri->base.info = Dinosaur_info;

    return tri;
}

// Main function to test
int main() {
    Dinosaur* dino1 = (Dinosaur*)TRex_new(68, 12.3);
    Dinosaur* dino2 = (Dinosaur*)Triceratops_new(68, 9.0);

    dino1->info(dino1);
    dino1->roar(dino1);

    dino2->info(dino2);
    dino2->roar(dino2);

    // Cast back to derived types to access specific methods
    TRex* trex = (TRex*)dino1;
    TRex_hunt(trex);

    Triceratops* tri = (Triceratops*)dino2;
    Triceratops_defend(tri);

    free(trex);
    free(tri);

    return 0;
}
