
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

// need to convert string to integers...

// hash function declaration 
int hash(int key);

int main(void)
{
    char string[42];
    
    printf("enter an integer to hash:\n");
    scanf("%s", string);
    printf("string is:%s\n", string);
    int i = atoi(string);
    printf("%i\n", i);
    int result = hash(i);
    printf("result is %i\n", result);
}

// hash function
int hash(int key)
{
    // multiplication method (data structures text)
    int result = 200 * (key * fmod(0.618033, 1));
    return result;
}
