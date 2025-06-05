#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Forward declaration for polymorphic methods
struct Dinosaur;

// Dinosaur "interface" (abstract base class) with function pointers
typedef struct DinosaurVTable {
    void (*roar)(struct Dinosaur*);
    void (*move)(struct Dinosaur*);
    void (*eat)(struct Dinosaur*, const char* food);
    void (*info)(struct Dinosaur*);
    void (*destroy)(struct Dinosaur*);
} DinosaurVTable;

// Base Dinosaur struct
typedef struct Dinosaur {
    DinosaurVTable* vtable;
    char* name;
    int age;           // millions of years ago
    double length;     // meters
} Dinosaur;

// Generic Dinosaur methods
void Dinosaur_roar(Dinosaur* dino) {
    printf("%s roars loudly!\n", dino->name);
}

void Dinosaur_move(Dinosaur* dino) {
    printf("%s moves slowly.\n", dino->name);
}

void Dinosaur_eat(Dinosaur* dino, const char* food) {
    printf("%s eats %s.\n", dino->name, food);
}

void Dinosaur_info(Dinosaur* dino) {
    printf("Dinosaur: %s\n", dino->name);
    printf("Age: %d million years ago\n", dino->age);
    printf("Length: %.2f meters\n", dino->length);
}

void Dinosaur_destroy(Dinosaur* dino) {
    free(dino->name);
    free(dino);
}

// --- T-Rex class ---
typedef struct TRex {
    Dinosaur base;
    int bite_force;  // new field
} TRex;

void TRex_roar(Dinosaur* dino) {
    printf("%s lets out a terrifying, bone-crushing roar!\n", dino->name);
}

void TRex_move(Dinosaur* dino) {
    printf("%s stomps powerfully across the land.\n", dino->name);
}

void TRex_eat(Dinosaur* dino, const char* food) {
    printf("%s devours %s with ferocious appetite.\n", dino->name, food);
}

void TRex_info(Dinosaur* dino) {
    TRex* trex = (TRex*)dino;
    Dinosaur_info(dino);
    printf("Bite Force: %d PSI\n", trex->bite_force);
}

void TRex_destroy(Dinosaur* dino) {
    // Nothing special to free beyond base
    Dinosaur_destroy(dino);
}

DinosaurVTable TRex_vtable = {
    TRex_roar,
    TRex_move,
    TRex_eat,
    TRex_info,
    TRex_destroy
};

TRex* TRex_new(int age, double length, int bite_force) {
    TRex* trex = malloc(sizeof(TRex));
    trex->base.vtable = &TRex_vtable;
    trex->base.name = strdup("T-Rex");
    trex->base.age = age;
    trex->base.length = length;
    trex->bite_force = bite_force;
    return trex;
}

// --- Triceratops class ---
typedef struct Triceratops {
    Dinosaur base;
    int horn_length;  // meters
} Triceratops;

void Triceratops_roar(Dinosaur* dino) {
    printf("%s makes a deep grunt.\n", dino->name);
}

void Triceratops_move(Dinosaur* dino) {
    printf("%s walks steadily with heavy steps.\n", dino->name);
}

void Triceratops_eat(Dinosaur* dino, const char* food) {
    printf("%s grazes peacefully on %s.\n", dino->name, food);
}

void Triceratops_info(Dinosaur* dino) {
    Triceratops* tri = (Triceratops*)dino;
    Dinosaur_info(dino);
    printf("Horn Length: %d meters\n", tri->horn_length);
}

void Triceratops_destroy(Dinosaur* dino) {
    Dinosaur_destroy(dino);
}

DinosaurVTable Triceratops_vtable = {
    Triceratops_roar,
    Triceratops_move,
    Triceratops_eat,
    Triceratops_info,
    Triceratops_destroy
};

Triceratops* Triceratops_new(int age, double length, int horn_length) {
    Triceratops* tri = malloc(sizeof(Triceratops));
    tri->base.vtable = &Triceratops_vtable;
    tri->base.name = strdup("Triceratops");
    tri->base.age = age;
    tri->base.length = length;
    tri->horn_length = horn_length;
    return tri;
}

// --- Velociraptor class ---
typedef struct Velociraptor {
    Dinosaur base;
    int speed;  // km/h
} Velociraptor;

void Velociraptor_roar(Dinosaur* dino) {
    printf("%s lets out a high-pitched screech!\n", dino->name);
}

void Velociraptor_move(Dinosaur* dino) {
    Velociraptor* velo = (Velociraptor*)dino;
    printf("%s runs swiftly at %d km/h.\n", dino->name, velo->speed);
}

void Velociraptor_eat(Dinosaur* dino, const char* food) {
    printf("%s quickly scavenges %s.\n", dino->name, food);
}

void Velociraptor_info(Dinosaur* dino) {
    Velociraptor* velo = (Velociraptor*)dino;
    Dinosaur_info(dino);
    printf("Speed: %d km/h\n", velo->speed);
}

void Velociraptor_destroy(Dinosaur* dino) {
    Dinosaur_destroy(dino);
}

DinosaurVTable Velociraptor_vtable = {
    Velociraptor_roar,
    Velociraptor_move,
    Velociraptor_eat,
    Velociraptor_info,
    Velociraptor_destroy
};

Velociraptor* Velociraptor_new(int age, double length, int speed) {
    Velociraptor* velo = malloc(sizeof(Velociraptor));
    velo->base.vtable = &Velociraptor_vtable;
    velo->base.name = strdup("Velociraptor");
    velo->base.age = age;
    velo->base.length = length;
    velo->speed = speed;
    return velo;
}

// --- Dinosaur Zoo ---
typedef struct Zoo {
    Dinosaur** dinosaurs;
    int capacity;
    int count;
} Zoo;

Zoo* Zoo_new(int capacity) {
    Zoo* zoo = malloc(sizeof(Zoo));
    zoo->dinosaurs = malloc(sizeof(Dinosaur*) * capacity);
    zoo->capacity = capacity;
    zoo->count = 0;
    return zoo;
}

void Zoo_add(Zoo* zoo, Dinosaur* dino) {
    if (zoo->count < zoo->capacity) {
        zoo->dinosaurs[zoo->count++] = dino;
    } else {
        printf("Zoo is full!\n");
    }
}

void Zoo_show_all(Zoo* zoo) {
    printf("\n--- Dinosaur Zoo Info ---\n");
    for (int i = 0; i < zoo->count; i++) {
        zoo->dinosaurs[i]->vtable->info(zoo->dinosaurs[i]);
        zoo->dinosaurs[i]->vtable->roar(zoo->dinosaurs[i]);
        zoo->dinosaurs[i]->vtable->move(zoo->dinosaurs[i]);
        zoo->dinosaurs[i]->vtable->eat(zoo->dinosaurs[i], "plants or meat");
        printf("\n");
    }
}

void Zoo_destroy(Zoo* zoo) {
    for (int i = 0; i < zoo->count; i++) {
        zoo->dinosaurs[i]->vtable->destroy(zoo->dinosaurs[i]);
    }
    free(zoo->dinosaurs);
    free(zoo);
}

// --- Main ---
int main() {
    Zoo* myZoo = Zoo_new(5);

    TRex* rex = TRex_new(68, 12.3, 12000);
    Triceratops* tri = Triceratops_new(68, 9.0, 2);
    Velociraptor* velo = Velociraptor_new(75, 2.0, 60);

    Zoo_add(myZoo, (Dinosaur*)rex);
    Zoo_add(myZoo, (Dinosaur*)tri);
    Zoo_add(myZoo, (Dinosaur*)velo);

    Zoo_show_all(myZoo);

    Zoo_destroy(myZoo);

    return 0;
}
