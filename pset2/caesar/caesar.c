#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

string plain;
int key;
int charref;

int main(int argc, string argv[])
{
    //if user does not provide a 2nd argument then return error
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    /* put second argument into key variable */
    key = atoi(argv[1]);
    
    /* prompt for plaintext and put into plain variable */
    printf("plaintext: ");
    plain = get_string();

    printf("ciphertext: ");
    for (int i = 0, j = strlen(plain); i < j; i++)
    {
    /* if char is alphabetical then convert to cipher and print */
        if (isalpha(plain[i]))
        {
            if (isupper(plain[i]))
            {
                printf("%c", (plain[i] - 'A' + key) % 26 + 'A');
            }
            if (islower(plain[i]))
            {
                printf("%c", (plain[i] - 'a' + key) % 26 + 'a');
            }
        }
    /* if char is not in the alphabet then do nothing and just print it*/
        else 
        {
            printf("%c", plain[i]);
        }
    }
printf("\n");
return 0;
}