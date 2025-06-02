#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Forward declaration
struct Animal;

typedef struct AnimalVTable {
    void (*speak)(struct Animal*);
    void (*show_color)(struct Animal*);
    void (*info)(struct Animal*);
    void (*destroy)(struct Animal*);
} AnimalVTable;

typedef struct Animal {
    AnimalVTable* vtable;
    char* name;
    char* color;
    char* habitat;
} Animal;

// Generic functions
void Animal_speak(Animal* animal) {
    printf("%s makes a generic animal sound.\n", animal->name);
}

void Animal_show_color(Animal* animal) {
    printf("%s has a %s color.\n", animal->name, animal->color);
}

void Animal_info(Animal* animal) {
    printf("Animal: %s\n", animal->name);
    printf("Habitat: %s\n", animal->habitat);
    animal->vtable->show_color(animal);
    animal->vtable->speak(animal);
}

void Animal_destroy(Animal* animal) {
    free(animal->name);
    free(animal->color);
    free(animal->habitat);
    free(animal);
}

// --- Pink Flamingo ---
typedef struct Flamingo {
    Animal base;
    int leg_length;
} Flamingo;

void Flamingo_speak(Animal* animal) {
    printf("%s honks softly.\n", animal->name);
}

void Flamingo_show_color(Animal* animal) {
    printf("%s is mostly pink with a graceful appearance.\n", animal->name);
}

void Flamingo_info(Animal* animal) {
    Flamingo* f = (Flamingo*)animal;
    Animal_info(animal);
    printf("Leg Length: %d cm\n", f->leg_length);
}

void Flamingo_destroy(Animal* animal) {
    Animal_destroy(animal);
}

AnimalVTable Flamingo_vtable = {
    Flamingo_speak,
    Flamingo_show_color,
    Flamingo_info,
    Flamingo_destroy
};

Flamingo* Flamingo_new() {
    Flamingo* f = malloc(sizeof(Flamingo));
    f->base.vtable = &Flamingo_vtable;
    f->base.name = strdup("Flamingo");
    f->base.color = strdup("pink");
    f->base.habitat = strdup("wetlands");
    f->leg_length = 80;
    return f;
}

// --- Pink Axolotl ---
typedef struct Axolotl {
    Animal base;
    char* skin_pattern;
} Axolotl;

void Axolotl_speak(Animal* animal) {
    printf("%s gurgles underwater.\n", animal->name);
}

void Axolotl_show_color(Animal* animal) {
    printf("%s has translucent pink skin with visible veins.\n", animal->name);
}

void Axolotl_info(Animal* animal) {
    Axolotl* ax = (Axolotl*)animal;
    Animal_info(animal);
    printf("Skin Pattern: %s\n", ax->skin_pattern);
}

void Axolotl_destroy(Animal* animal) {
    Axolotl* ax = (Axolotl*)animal;
    free(ax->skin_pattern);
    Animal_destroy(animal);
}

AnimalVTable Axolotl_vtable = {
    Axolotl_speak,
    Axolotl_show_color,
    Axolotl_info,
    Axolotl_destroy
};

Axolotl* Axolotl_new() {
    Axolotl* ax = malloc(sizeof(Axolotl));
    ax->base.vtable = &Axolotl_vtable;
    ax->base.name = strdup("Axolotl");
    ax->base.color = strdup("pink");
    ax->base.habitat = strdup("freshwater lakes");
    ax->skin_pattern = strdup("mottled with feathery gills");
    return ax;
}

// --- Not Pink Animal (e.g., Elephant) ---
typedef struct Elephant {
    Animal base;
    double trunk_length;
} Elephant;

void Elephant_speak(Animal* animal) {
    printf("%s trumpets loudly!\n", animal->name);
}

void Elephant_show_color(Animal* animal) {
    printf("%s is grey, not pink.\n", animal->name);
}

void Elephant_info(Animal* animal) {
    Elephant* e = (Elephant*)animal;
    Animal_info(animal);
    printf("Trunk Length: %.2f meters\n", e->trunk_length);
}

void Elephant_destroy(Animal* animal) {
    Animal_destroy(animal);
}

AnimalVTable Elephant_vtable = {
    Elephant_speak,
    Elephant_show_color,
    Elephant_info,
    Elephant_destroy
};

Elephant* Elephant_new() {
    Elephant* e = malloc(sizeof(Elephant));
    e->base.vtable = &Elephant_vtable;
    e->base.name = strdup("Elephant");
    e->base.color = strdup("grey");
    e->base.habitat = strdup("savannah");
    e->trunk_length = 2.1;
    return e;
}

// --- Gallery (Collection of Animals) ---
typedef struct Gallery {
    Animal** animals;
    int capacity;
    int count;
} Gallery;

Gallery* Gallery_new(int cap) {
    Gallery* g = malloc(sizeof(Gallery));
    g->animals = malloc(sizeof(Animal*) * cap);
    g->capacity = cap;
    g->count = 0;
    return g;
}

void Gallery_add(Gallery* g, Animal* a) {
    if (g->count < g->capacity) {
        g->animals[g->count++] = a;
    } else {
        printf("Gallery is full!\n");
    }
}

void Gallery_show_all(Gallery* g) {
    printf("\n--- Pink Animal Gallery ---\n");
    for (int i = 0; i < g->count; i++) {
        printf("\n[%d]\n", i + 1);
        g->animals[i]->vtable->info(g->animals[i]);
    }
}

void Gallery_destroy(Gallery* g) {
    for (int i = 0; i < g->count; i++) {
        g->animals[i]->vtable->destroy(g->animals[i]);
    }
    free(g->animals);
    free(g);
}

// --- Main ---
int main() {
    Gallery* pinkGallery = Gallery_new(5);

    Flamingo* flamingo = Flamingo_new();
    Axolotl* axolotl = Axolotl_new();
    Elephant* elephant = Elephant_new(); // Not pink but for contrast

    Gallery_add(pinkGallery, (Animal*)flamingo);
    Gallery_add(pinkGallery, (Animal*)axolotl);
    Gallery_add(pinkGallery, (Animal*)elephant);

    Gallery_show_all(pinkGallery);
    Gallery_destroy(pinkGallery);

    return 0;
}
