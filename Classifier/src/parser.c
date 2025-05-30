#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

#define INITIAL_CAPACITY 100

// Prototipos de funciones
void CLASSIFICATION();
void CODE();
void CLASSES();
void IDS();
void SEPS();
void SEPSPRIME();
void STATEMENTS();
void STATEMENTSPRIME();
void CONFIDENCE();

// Variables globales
char **tokens;
char *current_token = NULL; // Variable global para el token actual
int counter = 0;            // Contador para el número de tokens procesados
int max_tokens = 0;         // Variable para almacenar el número máximo de tokens
int OOP = 0;                // Variable para indicar si se encontró OOP
int PRO = 0;                // Variable para indicar si se encontró PRO
FILE *output_file = NULL;   // Archivo de salida para classification.txt

// Función para imprimir tanto a consola como a archivo
void txt_printf(const char *format, ...)
{
    va_list args1, args2;
    va_start(args1, format);
    va_copy(args2, args1);

    // Imprimir a archivo si está abierto
    if (output_file != NULL)
    {
        vfprintf(output_file, format, args2);
        fflush(output_file); // Asegurar que se escriba inmediatamente
    }

    va_end(args1);
    va_end(args2);
}

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

// Función para obtener el siguiente token
char *Get_NextToken()
{
    if (counter >= max_tokens)
    {
        printf("No hay mas tokens disponibles.\n");
        current_token = "$";
        return current_token; // No hay más tokens
    }
    current_token = tokens[counter];
    counter++;
    return current_token;
}

// Función para hacer match con un token específico
int Match(char *y)
{
    // Token actual es "$", significa que no hay más tokens
    if (current_token == "$")
    {
        printf("Clasificacion finalizada.\n");
        CONFIDENCE(); // No hay token actual
    }
    if (strcmp(current_token, y) == 0)
    {
        current_token = Get_NextToken();
        return 1; // Match exitoso
    }
    else
    {
        printf("Error: token '%s' no coincide con '%s'.\n", current_token, y);
        CONFIDENCE(); // Match fallido
    }
}

// Funcion para clasificar declaraciones prime
void STATEMENTSPRIME()
{
    if (strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0)
    {
        CLASSES();    // Clasificar clases
        STATEMENTS(); // Clasificar declaraciones
    }
    else if (strcmp(current_token, "1") == 0 || strcmp(current_token, "3") == 0)
    {
        SEPS();       // Clasificar separadores
        STATEMENTS(); // Clasificar declaraciones
    }
    else if (strcmp(current_token, "4") == 0 || strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0 || strcmp(current_token, "1") == 0 || strcmp(current_token, "3") == 0)
    {
        return; // EPSILON
    }
    else
    {
        printf("Error: token '%s' no coincide con ninguna regla de statementprime.\n", current_token);
        CONFIDENCE(); // Error
    }
}

// Funcion para clasificar declaraciones
void STATEMENTS()
{
    if (strcmp(current_token, "7") == 0 || strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0 || strcmp(current_token, "1") == 0)
    {
        IDS();             // Clasificar identificadores
        STATEMENTSPRIME(); // Clasificar declaraciones prime
    }
    else if (strcmp(current_token, "4") == 0 || strcmp(current_token, "$") == 0)
    {
        return; // EPSILON
    }
    else
    {
        printf("Error: token '%s' no coincide con ninguna regla de statements.\n", current_token);
        CONFIDENCE(); // Error
    }
}

// Funcion para clasificar separadores prime
void SEPSPRIME()
{
    if (strcmp(current_token, "3") == 0)
    {
        Match("3");   // Match {
        STATEMENTS(); // Clasificar declaraciones
        Match("4");   // Match }
    }
    else if (strcmp(current_token, "4") == 0 || strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0 || strcmp(current_token, "1") == 0 || strcmp(current_token, "3") == 0 || strcmp(current_token, "$") == 0 || strcmp(current_token, "7") == 0)
    {
        return; // EPSILON
    }
    else
    {
        printf("Error: token '%s' no coincide con ninguna regla de separadores prime.\n", current_token);
        CONFIDENCE(); // Error
    }
}

// Funcion para clasificar separadores
void SEPS()
{
    if (strcmp(current_token, "1") == 0)
    {
        Match("1");  // Match (
        IDS();       // Clasificar identificadores
        Match("2");  // Match )
        SEPSPRIME(); // Clasificar separadores prime
    }
    if (strcmp(current_token, "3") == 0)
    {
        Match("3");   // Match {
        STATEMENTS(); // Clasificar declaraciones
        Match("4");   // Match }
    }
}

// Funcion para clasificar identificadores
void IDS()
{
    if (strcmp(current_token, "7") == 0)
    {
        Match("7"); // Match identificador
        IDS();      // Clasificar identificadores
    }
    else if (strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0 || strcmp(current_token, "1") == 0 || strcmp(current_token, "3") == 0 || strcmp(current_token, "$") == 0 || strcmp(current_token, "2") == 0 || strcmp(current_token, "4") == 0)
    {
        return; // EPSILON
    }
    else
    {
        printf("Error: token '%s' no coincide con ninguna regla de identificadores.\n", current_token);
        CONFIDENCE(); // ERROR
    }
}

// Funcion para clasificar clases
void CLASSES()
{
    if (strcmp(current_token, "5") == 0)
    {
        Match("5"); // Match class
        IDS();      // Clasificar identificadores
        SEPS();     // Clasificar separadores
    }
    else if (strcmp(current_token, "6") == 0)
    {
        Match("6"); // Match struct
        IDS();      // Clasificar identificadores
        SEPS();     // Clasificar separadores
    }
}

// Funcion para clasificar el codigo
void CODE()
{
    if (strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0)
    {
        OOP = 1;   // Indicar que se encontró OOP
        CLASSES(); // Clasificar clases
        IDS();     // Clasificar identificadores
        CODE();    // Clasificar código
    }
    else if (strcmp(current_token, "1") == 0 || strcmp(current_token, "3") == 0)
    {
        PRO = 1; // Indicar que se encontró PRO
        SEPS();  // Clasificar separadores
        IDS();   // Clasificar identificadores
        CODE();  // Clasificar código
    }
    else if (strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0 || strcmp(current_token, "1") == 0 || strcmp(current_token, "3") == 0 || strcmp(current_token, "$") == 0)
    {
        return; // EPSILON
    }
    else
    {
        printf("Error: token '%s' no coincide con ninguna regla de código.\n", current_token);
        CONFIDENCE(); // Error
    }
}

// Funcion para empezar a clasificar
void CLASSIFICATION()
{
    IDS();  // Clasificar identificadores
    CODE(); // Clasificar código
}

// Funcion para imprimir la confianza en la clasificacion
void CONFIDENCE()
{
    printf("--------------------------------------------\n");
    if (OOP == 1 && PRO == 1)
    {
        printf("El codigo es hibrido.\n");
        txt_printf("Hibrido\n");
    }
    else if (OOP == 1)
    {
        printf("El codigo es OOP.\n");
        txt_printf("OOP\n");
    }
    else if (PRO == 1)
    {
        printf("El codigo es procedural.\n");
        txt_printf("Procedural\n");
    }
    else
    {
        printf("No se encontro codigo.\n");
        txt_printf("Texto\n");
    }
    printf("Tokens procesados: %d de %d\n", counter, max_tokens);
    printf("Confianza: %.2f%%\n", (float)counter / max_tokens * 100);
    txt_printf("%.2f%%\n", (float)counter / max_tokens * 100);

    // Cerrar archivo de salida
    if (output_file != NULL)
    {
        fclose(output_file);
        output_file = NULL;
    }

    exit(0); // Terminar el programa después de imprimir la confianza
}

int main()
{
    // Abrir archivo de salida para escritura
    output_file = fopen("classification.txt", "w");
    if (!output_file)
    {
        printf("Error: No se pudo crear el archivo classification.txt\n");
        return 1;
    }

    printf("--------------------------------------------\n");
    printf("Parser iniciado.\n");
    // ---------- Leer tokens.txt ----------
    FILE *tokens_file = fopen("tokens.txt", "r");
    if (!tokens_file)
    {
        printf("No se pudo abrir tokens.txt para lectura.\n");
        return 1;
    }

    tokens = malloc(INITIAL_CAPACITY * sizeof(char *));
    int tokens_size = 0, tokens_capacity = INITIAL_CAPACITY;

    char line[256];
    while (fgets(line, sizeof(line), tokens_file))
    {
        line[strcspn(line, "\r\n")] = 0;
        add_line(&tokens, &tokens_size, &tokens_capacity, line);
    }
    fclose(tokens_file);
    max_tokens = tokens_size; // Guardar el número máximo de tokens

    // ---------- Imprimir tokens ----------
    printf("Tokens leidos: %d\n", tokens_size);
    for (int i = 0; i < tokens_size; i++)
    {
        printf("%s\n", tokens[i]);
    }

    current_token = Get_NextToken(); // Inicializar el primer token
    CLASSIFICATION();                // Clasificar

    printf("Clasificacion finalizada.\n");

    printf("--------------------------------------------\n");
    // ---------- Imprimir resultados ----------
    printf("Resultados de la clasificacion:\n");
    printf("Valor de OOP: %d\n", OOP);
    printf("Valor de PRO: %d\n", PRO);

    // Empezar la clasificación
    CONFIDENCE(); // Imprimir confianza en la clasificación

    // ---------- Liberar memoria ----------
    for (int i = 0; i < tokens_size; i++)
        free(tokens[i]);

    return 0;
}
