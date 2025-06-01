#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[50];
    int priority;
} Task;

typedef struct {
    Task tasks[10];
    int count;
    void (*add)(struct Scheduler*, const char*, int);
    void (*run)(struct Scheduler*);
} Scheduler;

void addTask(Scheduler* s, const char* name, int priority) {
    if (s->count >= 10) return;
    strcpy(s->tasks[s->count].name, name);
    s->tasks[s->count].priority = priority;
    s->count++;
}

int compare(const void* a, const void* b) {
    return ((Task*)b)->priority - ((Task*)a)->priority;
}

void runTasks(Scheduler* s) {
    qsort(s->tasks, s->count, sizeof(Task), compare);
    for (int i = 0; i < s->count; i++) {
        printf("Running: %s (Priority %d)\n", s->tasks[i].name, s->tasks[i].priority);
    }
}

int main() {
    Scheduler sched = {.count = 0, .add = addTask, .run = runTasks};
    sched.add(&sched, "Update Firmware", 2);
    sched.add(&sched, "Backup Database", 5);
    sched.add(&sched, "Send Logs", 1);
    sched.run(&sched);
    return 0;
}
