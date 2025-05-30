// compiler.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TOKEN 500

// Definicion de la estructura del nodo de la lista ligada
struct Node
{
    char data[500];
    struct Node *next;
};

// Funcion para crear un nuevo nodo
struct Node *createNode(char data[])
{
    struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
    strcpy(newNode->data, data);
    newNode->next = NULL;
    return newNode;
}

// Funcion para insertar un nodo al final de la lista ligada
void insertAtEnd(struct Node **head, char data[])
{
    struct Node *newNode = createNode(data);
    if (*head == NULL)
    {
        *head = newNode;
        return;
    }
    struct Node *temp = *head;
    while (temp->next != NULL)
    {
        temp = temp->next;
    }
    temp->next = newNode;
}

// SYMBOL TABLE
struct Node *symbol_table = NULL;

// Funcion para verificar si un identificador ya existe en la tabla de simbolos
int exists_in_symbol_table(const char *id)
{
    struct Node *current = symbol_table;
    int count = 0;
    while (current != NULL)
    {
        count++;
        if (strcmp(current->data, id) == 0)
        {
            return count;
        }
        current = current->next;
    }
    return -1;
}

// Funcion para determinar si un caracter es una letra (a-z, A-Z)
int es_letra(char c)
{
    return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
}

// Funcion para determinar si un caracter es un digito (0-9)
int es_digito(char c)
{
    return (c >= '0' && c <= '9');
}

// Funcion para determinar si un caracter es alfanumerico (letras y digitos)
int es_alfanumerico(char c)
{
    return es_letra(c) || es_digito(c);
}

// Funcion para determinar si un caracter es un espacio en blanco
int es_espacio(char c)
{
    return c == ' ' || c == '\n' || c == '\t' || c == '\r';
}

// Funcion para determinar si un caracter es un delimitador
int es_delimitador(char c)
{
    return c == ';' || c == ',' || c == '.' || c == ':' || c == '=' ||
           c == '*' || c == '&' || c == '<' || c == '>' || c == '\'' ||
           c == '+' || c == '-' || c == '/' || c == '%' || c == '!' ||
           c == '~' || c == '^' || c == '|' || c == '?' || c == '#' ||
           c == '/' || c == '[' || c == ']' || c == '\\';
}

// Separadores del lenguaje
const char *separadores[] = {
    "(",
    ")",
    "{",
    "}",
};

// Palabras clave del lenguaje
const char *palabras_clave[] = {
    "class",
    "struct",
};

int keywordLength = sizeof(palabras_clave) / sizeof(palabras_clave[0]);
int separadorLength = sizeof(separadores) / sizeof(separadores[0]);

// Marcar el token de identificadores
int identifier_id = 1 + sizeof(separadores) / sizeof(separadores[0]) +
                    sizeof(palabras_clave) / sizeof(palabras_clave[0]);

// Contador de identificadores
int identifier_count = 0;

// Funcion que determina si un estado es un estado aceptador
int Accept(int estado)
{
    if (estado > 2 && estado < 9)
    {
        return 1;
    }
    return 0;
}

// Funcion que determina si un estado es un estado de error
int Error(int estado)
{
    return estado == 10;
}

// Tabla de transiciones del DFA
int TransitionTable[3][10] = {
    [0] = {1, 1, 0, 0, 3, 4, 5, 6, 2, 0}, // Estado de inicio
    [1] = {1, 1, 1, 7, 7, 7, 7, 7, 7, 7}, // Estado de identificador
    [2] = {2, 2, 2, 2, 2, 2, 2, 2, 0, 0}, // Estado de string
};

// Funcion que determina la columna de la tabla de transiciones segun el caracter
int char_to_col(char c)
{
    if (es_letra(c))
    {
        return 0;
    }
    if (c == '_')
    {
        return 1;
    }
    if (es_digito(c))
    {
        return 2;
    }
    if (es_espacio(c) || es_delimitador(c) || c == EOF)
    {
        return 3;
    }
    if (c == '(')
    {
        return 4;
    }
    if (c == ')')
    {
        return 5;
    }
    if (c == '{')
    {
        return 6;
    }
    if (c == '}')
    {
        return 7;
    }
    if (c == '"')
    {
        return 8;
    }
    return 9;
}

// Funcion que determina el nuevo estado del DFA segun el estado actual y el caracter
int T(int estado, char c)
{
    int col = char_to_col(c);
    return TransitionTable[estado][col];
}

// Funcion que determina si un estado puede seguir aceptando caracteres
int Advance(int estado, char c)
{
    if (Accept(estado))
        return 0;
    return 1;
}

// Funcion que escribe el token al archivo de tokens
void write_token(FILE *tokens_file, char *buffer, int index, int estado)
{
    buffer[index] = '\0';

    // Estados aceptadores de parentesis y llaves
    if (estado > 2 && estado < 7)
    {
        printf("%d\n", estado - 2);
        fprintf(tokens_file, "%d\n", estado - 2);
        return;
    }

    // Estado aceptador de identificadores
    if (estado == 7)
    {
        // printf("Token: %s\n", buffer);
        for (int i = 0; i < keywordLength; i++)
        {
            if (strcmp(buffer, palabras_clave[i]) == 0)
            {
                printf("%d\n", i + separadorLength + 1);
                fprintf(tokens_file, "%d\n", i + separadorLength + 1);
                return;
            }
        }

        int exists = exists_in_symbol_table(buffer);

        if (exists == -1)
        {
            insertAtEnd(&symbol_table, buffer); // SYMBOL TABLE: Agregar identificador
            identifier_count++;
            printf("%d, %d\n", identifier_id, identifier_count);
            // Se quita la tabla de simbolos para el parser
            fprintf(tokens_file, "%d\n", identifier_id);
        }
        else
        {
            printf("%d, %d\n", identifier_id, exists);
            fprintf(tokens_file, "%d\n", identifier_id);
        }

        return;
    }
}

int main(int argc, char *argv[])
{
    // Comprobar si se recibieron los argumentos minimos
    if (argc < 2)
    {
        printf("Uso: %s <archivo>\n", argv[0]);
        return 1;
    }

    // Abrir archivo de tokens en modo escritura
    FILE *tokens_file = fopen("tokens.txt", "w");
    if (!tokens_file)
    {
        printf("No se pudo abrir tokens.txt para escritura.\n");
        return 1;
    }

    // Abrir el archivo de entrada
    FILE *archivo = fopen(argv[1], "rb");
    if (!archivo)
    {
        printf("No se pudo abrir el archivo de lectura.\n");
        fclose(tokens_file);
        return 1;
    }

    printf("Leyendo el archivo: %s\n", argv[1]);

    // Inicializar variables
    char c, buffer[MAX_TOKEN];
    int index = 0;

    // Leer el primer caracter del archivo
    c = fgetc(archivo);
    while (c != EOF)
    {

        // Inicializar el estado del DFA en INICIO
        int estado = 0;
        // Reiniciar el buffer
        index = 0;

        while (!Accept(estado) && !Error(estado))
        {
            // Determinar el nuevo estado del DFA
            estado = T(estado, c);
            // Guardar el caracter en el buffer
            if (estado != 0)
            {
                buffer[index++] = c;
            }
            // printf("Estado: %d, Caracter: %c\n", estado, c);

            if (Advance(estado, c))
            {
                // Leer el siguiente caracter
                c = fgetc(archivo);
                if ((unsigned char)c == 255)
                    break; // evitar pasar EOF a T()
            }
        }

        if (index == 0)
            break;

        // El estado es aceptador o de error
        if (Accept(estado))
        {
            // Si el caracter es un espacio, ignorarlo
            if (es_espacio(buffer[0]))
            {
                c = fgetc(archivo);
                continue;
            }

            // Si el estado es 7 (aceptor de identificador)
            if (estado == 7)
            {
                // Ignorar el ultimo caracter
                index--;
                // Devolver el caracter al flujo de entrada
                ungetc(c, archivo);
            }

            // Escribir el token al archivo
            write_token(tokens_file, buffer, index, estado);
            c = fgetc(archivo);
        }
        else if (Error(estado))
        {
            printf("Token: ");
            for (int i = 0; i < index; i++)
            {
                printf("%c", buffer[i]);
            }

            printf("Error: token no reconocido.\n");
            fclose(archivo);
            fclose(tokens_file);
            return 0;
        }
    }

    // Escribir tabla de simbolos a archivo
    FILE *symtab_file = fopen("symbols.txt", "w");
    if (!symtab_file)
    {
        printf("No se pudo abrir symbol_table.txt para escritura.\n");
        return 1;
    }

    struct Node *current = symbol_table;
    int entry = 1;
    while (current != NULL)
    {
        fprintf(symtab_file, "%d: %s\n", entry++, current->data);
        current = current->next;
    }

    // Cerrar archivos
    fclose(archivo);
    fclose(tokens_file);
    fclose(symtab_file);
    return 0;
}