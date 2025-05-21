#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 100

// Función para agregar una línea a un arreglo dinámico de cadenas
void add_line(char ***arr, int *size, int *capacity, const char *line)
{
    if (*size >= *capacity)
    {
        *capacity *= 2;
        *arr = realloc(*arr, (*capacity) * sizeof(char *));
        if (!*arr)
        {
            perror("Realloc failed");
            exit(1);
        }
    }
    (*arr)[*size] = strdup(line);
    (*size)++;
}

int main()
{
    // ---------- Leer tokens.txt ----------
    FILE *tokens_file = fopen("tokens.txt", "r");
    if (!tokens_file)
    {
        printf("No se pudo abrir tokens.txt para lectura.\n");
        return 1;
    }

    char **tokens = malloc(INITIAL_CAPACITY * sizeof(char *));
    int tokens_size = 0, tokens_capacity = INITIAL_CAPACITY;

    char line[256];
    while (fgets(line, sizeof(line), tokens_file))
    {
        line[strcspn(line, "\r\n")] = 0;
        add_line(&tokens, &tokens_size, &tokens_capacity, line);
    }
    fclose(tokens_file);

    // ---------- Leer symbol_table.txt ----------
    FILE *symtab_file = fopen("symbols.txt", "r");
    if (!symtab_file)
    {
        printf("No se pudo abrir symbols.txt para lectura.\n");
        return 1;
    }

    char **symbols = malloc(INITIAL_CAPACITY * sizeof(char *));
    int symbols_size = 0, symbols_capacity = INITIAL_CAPACITY;

    while (fgets(line, sizeof(line), symtab_file))
    {
        line[strcspn(line, "\r\n")] = 0;
        add_line(&symbols, &symbols_size, &symbols_capacity, line);
    }
    fclose(symtab_file);

    // ---------- Imprimir tokens ----------
    printf("Tokens leidos: %d\n", tokens_size);
    for (int i = 0; i < tokens_size; i++)
    {
        printf("%s\n", tokens[i]);
    }

    // ---------- Imprimir símbolos ----------
    printf("\nSimbolos leidos: %d\n", symbols_size);
    for (int i = 0; i < symbols_size; i++)
    {
        printf("%s\n", symbols[i]);
    }

    // ---------- Liberar memoria ----------
    for (int i = 0; i < tokens_size; i++)
        free(tokens[i]);
    for (int i = 0; i < symbols_size; i++)
        free(symbols[i]);
    free(tokens);
    free(symbols);

    return 0;
}
