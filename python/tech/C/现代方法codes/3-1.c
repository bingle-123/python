#include <stdio.h>

int count_space(const char *);
void print_array(int[], int);
int main()
{
    char *a = "123123123";
    printf("%d;", count_space(" asdfasd asdfasdfd asdfasd"));
    // printf("%c", a[0]);
    // printf("%c", *(a+1));
    // printf("%c", *(a+2));
    // printf("%c", *(a+3));
    // int a[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}, *p;
    // for (p = a; p < a + 9;p++)
    // {
    //     printf("old %d ;", *p);
    //     printf("new %d ;\n", ++(*p));
    // }

    // print_array(a, 10);
    return 0;
}
int count_space(const char *s){
    int count=0;
    for(;*s!='\0';s++){
        if(*s==' '){
            count++;
        }
    }
    return count;
}

void print_array(int a[], int len)
{
    int i;
    for (i = 0; i < len; i++)
    {
        printf("%d ", a[i]);
    }
}