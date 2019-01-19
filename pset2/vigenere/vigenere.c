#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>


// define variables
string plain;
string key;
int mod;
int alpha;

int main(int argc, string argv[])
{
    /*if user does not provide a 2nd argument then return error*/
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    
    /* put second argument into key variable and store length of
    argument string in mod variable*/
    key = argv[1];
    mod = strlen(argv[1]);
    
    /* if key does not consist of all alpha characters then error */
    for (alpha = 0; isalpha(key[alpha]);)
    {
        alpha++;
    }
    if (alpha != mod)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    
    /* prompt for plaintext until user provides a string */
    do
    {
    printf("plaintext: ");
    plain = get_string();
    }
    while (strlen(plain) < 1);
    
    /* start printing the cipher text */ 
    printf("ciphertext: ");
    for (int i = 0, j = strlen(plain), k = 0; i < j; i++)
    {
        /* calculate key value */
        int keyval = tolower(key[k % mod]) - 'a';
        /*check if item is a character */
        if (isalpha(plain[i]))
        {
                if (isupper(plain[i]))
                {
                    printf("%c", (plain[i] - 'A' + keyval) % 26 + 'A');
                    k++;
                }
                if (islower(plain[i]))
                {
                    printf("%c", (plain[i] - 'a' + keyval) % 26 + 'a');
                    k++;
                }
        }
        /* if no character then do nothing and just print it */
        else 
        {
            printf("%c", plain[i]);
        } 
    } 
    
printf("\n");
return 0;
}