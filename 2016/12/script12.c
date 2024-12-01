#include <stdio.h>


#define PART2


int main(void) {
    int a = 0; int b = 0; int c = 0; int d = 0;
    
    #ifdef PART2
    c = 1;
    #endif
    
    // -----------
    a = 1;
    b = 1;
    d = 26;
    if (c != 0)
        goto l0;
    goto l1;
    l0:
    c = 7;
    l2:
    d += 1;
    c -= 1;
    if (c != 0)
        goto l2;
    l1:
    l4:
    c = a;
    l3:
    a += 1;
    b -= 1;
    if (b != 0)
        goto l3;
    b = c;
    d -= 1;
    if (d != 0)
        goto l4;
    c = 19;
    l6:
    d = 14;
    l5:
    a += 1;
    d -= 1;
    if (d != 0)
        goto l5;
    c -= 1;
    if (c != 0)
        goto l6;
    // ------------
    
    printf("%d\n", a);
    return 0;
}
