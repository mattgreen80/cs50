#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main (void)
{
/*check input, define variables and functions*/
    float fchg;
    int ichg;
    int greedy(int change);
    do
    {
        printf("Change owed:");
        fchg = get_float();
    }
    while(fchg <= 0);
/*convert input from dollars to cents and then give result via greedy function*/
    ichg = round(fchg * 100);
    printf("%i\n",greedy(ichg));
return 0;
}
/*function to provide coins used*/
int greedy(int change)
{
    int count = 0;
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    while(change / quarter >= 1)
    {
        count++;
        change = change - quarter;
    }
    while(change / dime >= 1)
    {
        count++;
        change = change - dime;
    }
    while(change / nickel >= 1)
    {
        count++;
        change = change - nickel;
    }
    while(change / penny >= 1)
    {
        count++;
        change = change - penny;
    }
return count;
}
