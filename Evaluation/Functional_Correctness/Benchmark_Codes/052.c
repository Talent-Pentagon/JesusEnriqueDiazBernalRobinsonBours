#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char title[50];
    char author[50];
} Book;

typedef struct Library {
    Book* books;
    int count;
    void (*add)(struct Library*, const char*, const char*);
    Book* (*find)(struct Library*, const char*);
} Library;

void addBook(Library* lib, const char* title, const char* author) {
    Book* new_books = realloc(lib->books, sizeof(Book) * (lib->count + 1));
    if (!new_books) {
        fprintf(stderr, "Memory allocation failed\n");
        return;
    }
    lib->books = new_books;

    strncpy(lib->books[lib->count].title, title, sizeof(lib->books[lib->count].title) - 1);
    lib->books[lib->count].title[sizeof(lib->books[lib->count].title) - 1] = '\0';

    strncpy(lib->books[lib->count].author, author, sizeof(lib->books[lib->count].author) - 1);
    lib->books[lib->count].author[sizeof(lib->books[lib->count].author) - 1] = '\0';

    lib->count++;
}

Book* findBook(Library* lib, const char* title) {
    for (int i = 0; i < lib->count; i++) {
        if (strcmp(lib->books[i].title, title) == 0) {
            return &lib->books[i];
        }
    }
    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <book title>\n", argv[0]);
        return 1;
    }

    Library lib = {NULL, 0, addBook, findBook};
    lib.add(&lib, "1984", "Orwell");
    lib.add(&lib, "Dune", "Herbert");

    Book* found = lib.find(&lib, argv[1]);
    if (found)
        printf("Found: %s by %s\n", found->title, found->author);
    else
        printf("Book not found.\n");

    free(lib.books);
    return 0;
}

