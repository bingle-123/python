#include <stdio.h>
#define XXX  "ddd"
#if !defined(XXX)
#error defined XXX
#endif

int main()
{
    printf("file %s\n", __FILE__);
    printf("date %s\n", __DATE__);
    printf("time %s\n", __TIME__);
    printf("line %d\n", __LINE__);
    printf("line %s\n",XXX);
    return 0;
}