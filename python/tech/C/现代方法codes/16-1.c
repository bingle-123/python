#include <stdio.h>

typedef struct
{
    int age;
    char *name;
    char *address;
} Info;

typedef enum { False,
               True } Bool;
Bool a = True;
Bool b = False;

typedef struct
{
    enum
    {
        Int = 0,
        Float = 1
    } kind;
    union {
        int i;
        float f;
    } u;
} Number;

Number n = {Int, {10}};
void print_info(Info);
int main()
{

    Info infos[10], *link;
    Info a = {20, "name1", "address1"};
    infos[0] = a;
    infos[1] = a;
    print_info(infos[1]);
    infos[1].age = 10;
    infos[2] = a;
    print_info(infos[2]);
    a.age = 10;
    print_info(infos[2]);
    print_info(a);
    link = infos;

    printf("%d", n.kind);
    return 0;
}
void print_info(Info info)
{
    printf("age: %d; ", info.age);
    printf("name: %s; ", info.name);
    printf("address: %s\n", info.address);
}
