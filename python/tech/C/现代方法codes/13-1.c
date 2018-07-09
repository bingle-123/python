#include <stdio.h>
#include <string.h>

int main()
{
    char *a, *b = "bbbb";
    strcpy(a, b);
    printf("%s \n", a);
    strcat(a, b);
    printf("%s \n", a);
    return 0;
}