#include <stdio.h>
#include <stdlib.h>

typedef struct Node Node;
struct Node
{
    int value;
    Node *next;
};

int main()
{
    Node *first = malloc(10 * sizeof(Node));
    Node new = {10, NULL};
    first[0] = new;
    first[1] = new;
    first[1].value = 20;
    first[1].next = &first[0];
    printf("%d", first[1].next->value);
    return 0;
}