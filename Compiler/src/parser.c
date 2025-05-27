#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 100

// Prototipos de funciones
// void PRO();
// void FUN();
// void CLASSESPRIME();
// void OOP();
// void OOPPRODS(int x);
void CLASSIFICATION();
void CODE();
void CLASSES();
void IDS();
void SEPS();
void STATEMENTS();
void STATEMENTSPRIME();


char **tokens;
char *current_token = NULL; // Variable global para el token actual
int counter = 0; // Contador para el número de tokens procesados
int max_tokens = 0; // Variable para almacenar el número máximo de tokens
int OOP = 0; // Variable para indicar si se encontró OOP
int PRO = 0; // Variable para indicar si se encontró PRO


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

char *Get_NextToken() {
    if (counter >= max_tokens) {
        printf("No hay mas tokens disponibles.\n");
        current_token = "$";
        return current_token; // No hay más tokens
    }
    current_token = tokens[counter];
    printf("Token actual: %s\n", current_token);
    counter++;
    return current_token;
}

int Match(char *y) {
    if(strcmp(current_token, y) == 0) {
        printf("Token '%s' match con '%s'\n", current_token, y);
        current_token = Get_NextToken();
        return 1; // Match exitoso
    }
    else{
        // printf("Error: token '%s' no coincide con '%s'\n", current_token, y);
        return 0; // Match fallido
    }
}


void STATEMENTSPRIME(){
    if(strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0){
        CLASSES(); // Clasificar clases
        STATEMENTS(); // Clasificar declaraciones
    }
    else if(strcmp(current_token, "1") == 0 || strcmp(current_token, "3") == 0){
        SEPS(); // Clasificar separadores
        STATEMENTS(); // Clasificar declaraciones
    }
    else{
        return; // EPSILON
    }
}

void STATEMENTS(){
    if(strcmp(current_token, "23") == 0 || strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0 || strcmp(current_token, "1") == 0){
        IDS(); // Clasificar identificadores
        STATEMENTSPRIME(); // Clasificar declaraciones
    }
    else{
        return; // EPSILON
    }
}

void SEPS(){
    if(strcmp(current_token, "1") == 0){
        Match("1"); // Match (
        IDS(); // Clasificar identificadores
        Match("2"); // Match )
        Match("3"); // Match {
        STATEMENTS(); // Clasificar declaraciones
        Match("4"); // Match }
    }
    if(strcmp(current_token, "3") == 0){
        Match("3"); // Match {
        STATEMENTS(); // Clasificar declaraciones
        Match("4"); // Match }
    }
}

void IDS(){
    if(strcmp(current_token, "23") == 0){
        Match("23");
        IDS();
    }
    else{
        return; // EPSILON
    }
}

void CLASSES(){
    if(strcmp(current_token, "5") == 0){
        Match("5"); // Match class
        IDS(); // Clasificar identificadores
        SEPS(); // Clasificar separadores
    }
    else if(strcmp(current_token, "6") == 0){
        Match("6"); // Match struct
        IDS(); // Clasificar identificadores
        SEPS(); // Clasificar separadores
    }
}

void CODE() {
    if(strcmp(current_token, "5") == 0 || strcmp(current_token, "6") == 0){
        CLASSES();
        IDS();
        CODE();
        OOP = 1; // Indicar que se encontró OOP
    }
    else if(strcmp(current_token, "1") == 0){
        SEPS();
        IDS();
        CODE();
        PRO = 1; // Indicar que se encontró PRO
    }
    else{
        return; // EPSILON
    }
}

void CLASSIFICATION(){
    IDS(); // Clasificar identificadores
    CODE();
    printf("Clasificacion completada.\n");
}


int main()
{
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
    CLASSIFICATION(); // Clasificar

    printf("Clasificacion finalizada.\n");

    printf("--------------------------------------------\n");
    // ---------- Imprimir resultados ----------
    printf("Resultados de la clasificacion:\n");
    printf("Valor de OOP: %d\n", OOP);
    printf("Valor de PRO: %d\n", PRO);

    if(OOP == 1 && PRO == 1){
        printf("El codigo es hibrido.\n");
    }
    else if(OOP == 1){
        printf("El codigo es OOP.\n");
    }
    else if(PRO == 1){
        printf("El codigo es procedural.\n");
    }
    else{
        printf("No se encontro codigo.\n");
    }


    // ---------- Liberar memoria ----------
    for (int i = 0; i < tokens_size; i++)
        free(tokens[i]);

    return 0;
}
