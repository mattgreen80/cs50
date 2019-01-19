// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

//structs here (e.g. node)
typedef struct node
{
    char word [LENGTH+1];
    struct node *next;
} 
node;

// Prototypes
bool check(const char *word);
bool load(const char *dictionary);
unsigned int size(void);
bool unload(void);
// hash function declaration 
int hash(const char* key);

#endif // DICTIONARY_H
