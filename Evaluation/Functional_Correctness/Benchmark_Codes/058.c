#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 5

typedef struct {
    char messages[MAX][100];
    int head, tail, count;
    void (*enqueue)(struct Queue*, const char*);
    void (*print)(struct Queue*);
} Queue;

void enqueue(Queue* q, const char* msg) {
    if (q->count == MAX) {
        q->head = (q->head + 1) % MAX;
        q->count--;
    }
    strcpy(q->messages[q->tail], msg);
    q->tail = (q->tail + 1) % MAX;
    q->count++;
}

void printMessages(Queue* q) {
    for (int i = 0, idx = q->head; i < q->count; i++) {
        printf("Msg: %s\n", q->messages[idx]);
        idx = (idx + 1) % MAX;
    }
}

int main() {
    Queue q = {.head = 0, .tail = 0, .count = 0, .enqueue = enqueue, .print = printMessages};

    char buffer[100];
    printf("Enter up to %d messages (empty line to stop):\n", MAX * 2);

    while (fgets(buffer, sizeof(buffer), stdin)) {
        // Remove trailing newline
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len-1] == '\n') {
            buffer[len-1] = '\0';
            len--;
        }
        if (len == 0) {
            // Empty line means stop reading
            break;
        }
        q.enqueue(&q, buffer);
    }

    printf("\nQueue contents:\n");
    q.print(&q);

    return 0;
}
