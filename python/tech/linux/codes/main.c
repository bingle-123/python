#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    int fd = create('test', 644);
    close(fd);
    return 0;
}