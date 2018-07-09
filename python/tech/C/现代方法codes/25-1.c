#include <stdio.h>
#include <locale.h>

int main()
{
    struct lconv *c;
    setlocale(LC_ALL,"");
    c = localeconv();
    printf("decimal_point: %s \n", c->decimal_point);
    printf("thousands_sep: %s \n", c->thousands_sep);
    printf("grouping: %s \n", c->grouping);
    printf("int_curr_symbol: %s \n", c->int_curr_symbol);
    printf("int_curr_symbol: %s \n", c->int_curr_symbol);
    printf("currency_symbol: %s \n", c->currency_symbol);
    printf("mon_decimal_point: %s \n", c->mon_decimal_point);
    printf("mon_thousands_sep: %s \n", c->mon_thousands_sep);
    printf("mon_grouping: %s \n", c->mon_grouping);
    printf("positive_sign: %s \n", c->positive_sign);
    printf("negative_sign: %s \n", c->negative_sign);
    return 0;
}