#include <stdio.h>
#include <cs50.h>

int main (void)
{
/* Check input and define variables */
    int height;
    int row;
    int space;
    int lhash;
    int rhash;
    do
    {
        printf("Height:");
        height = get_int();
    }
    while (height > 23 || height < 0);
    /* Keep track of row. Add one to height and set row at one so spaces can be calculated accurately */
    for (row = 1; row < (height +1); row++)
    {
        /* Draw first half of pyramid */
        for (space = (height - row); space > 0 ; space--)
        {
          printf(" ");
        }
        for (lhash = 1; lhash <= row; lhash++)
        {
            printf("#");
        }
        /* Print spaces between halves */
        printf("  ");
        /* Draw second half of pyramid */
        for (rhash = 1; rhash <= row; rhash++)
        {
            printf("#");
        }
        printf("\n");
    }
return 0;
}