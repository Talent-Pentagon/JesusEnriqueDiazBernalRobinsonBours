#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Item {
    char name[30];
    int quantity;
} Item;

typedef struct Inventory {
    Item* items;
    int size;
    int capacity;
    void (*add)(struct Inventory*, const char*, int);
    void (*restock)(struct Inventory*, const char*, int);
} Inventory;

void addItem(Inventory* inv, const char* name, int qty) {
    for (int i = 0; i < inv->size; i++) {
        if (strcmp(inv->items[i].name, name) == 0) {
            inv->items[i].quantity += qty;
            return;
        }
    }
    if (inv->size == inv->capacity) {
        inv->capacity = (inv->capacity == 0) ? 2 : inv->capacity * 2;
        inv->items = realloc(inv->items, inv->capacity * sizeof(Item));
    }
    strncpy(inv->items[inv->size].name, name, sizeof(inv->items[inv->size].name) - 1);
    inv->items[inv->size].name[sizeof(inv->items[inv->size].name) - 1] = '\0';
    inv->items[inv->size].quantity = qty;
    inv->size++;
}

void restockItem(Inventory* inv, const char* name, int qty) {
    for (int i = 0; i < inv->size; i++) {
        if (strcmp(inv->items[i].name, name) == 0) {
            inv->items[i].quantity += qty;
            return;
        }
    }
    addItem(inv, name, qty);
}

int getItemQuantity(Inventory* inv, const char* name) {
    for (int i = 0; i < inv->size; i++) {
        if (strcmp(inv->items[i].name, name) == 0) {
            return inv->items[i].quantity;
        }
    }
    return -1;
}

Inventory createInventory() {
    Inventory inv = {NULL, 0, 0, addItem, restockItem};
    return inv;
}

void destroyInventory(Inventory* inv) {
    free(inv->items);
    inv->items = NULL;
    inv->size = 0;
    inv->capacity = 0;
}

int main() {
    Inventory inv = createInventory();
    char command[20];
    char name[30];
    int qty;

    while (scanf("%s", command) != EOF) {
        if (strcmp(command, "add") == 0) {
            scanf("%s %d", name, &qty);
            inv.add(&inv, name, qty);
        } else if (strcmp(command, "restock") == 0) {
            scanf("%s %d", name, &qty);
            inv.restock(&inv, name, qty);
        } else if (strcmp(command, "get") == 0) {
            scanf("%s", name);
            printf("%d\n", getItemQuantity(&inv, name));
            fflush(stdout);
        } else if (strcmp(command, "exit") == 0) {
            break;
        }
    }

    destroyInventory(&inv);
    return 0;
}
