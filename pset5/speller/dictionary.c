// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#include "dictionary.h"

// number of "buckets" the hash table will use
#define BUCKETS 26

// global array of struct pointers (hash table)
node *hashtable[BUCKETS+1];

// Returns true if word is in dictionary else false.
bool check(const char *word)
{
    // copy word into temp array
    char string[LENGTH+1];
    // convert to lowercase
    for (int i = 0; i < strlen(word); i++)
    {
        string[i] = tolower(word[i]);
    }
    string[strlen(word)] = '\0';

    // hash word to get key and then create pointer to the node on the hash table where it should be
    node *cur = hashtable[hash(word)];

    // if there is no node return false
    if (cur == NULL)
    {
        return false;
    }
    // traverse list looking for matching word
    while (cur->next != NULL)
    {
        // if word is the same, then return true.
        if (strcmp(cur->word,string) == 0)
        {
            return true;
        }
        cur = cur->next;
    }
    // check last node
    if (cur->next == NULL)
    {
        // if word is the same, then return true.
        if (strcmp(cur->word,string) == 0)
        {
            return true;
        }
    }
    return false;
}

// Loads dictionary into memory, returning true if successful else false.
bool load(const char *dictionary)
{
    // initialize hash table (array of node pointers).
    for (int i = 0; i < BUCKETS+1; i++)
    {
        hashtable[i] = NULL;
    }
    //fopen dictionary file. function passes string name of dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    // word buffer
    char word[LENGTH+1];

    //scan dictionary for each word.
    while (fscanf(file, "%s", word) != EOF)
    {
            // for each iteration (word), create a node and copy word into it
            node *temp = malloc(sizeof(node));
            if (temp == NULL)
            {
                return false;
            }
            // copy string into the word member of the node struct
            strcpy(temp->word, word);
            // link up with the first node on the list or if this is the first node, start will be NULL
            temp->next = hashtable[hash(word)];
            // now change the new nodes pointer to make it the new first node
            hashtable[hash(word)] = temp;
    }

    // close dictionary after load
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded.
unsigned int size(void)
{
    // keep track of words
    int size = 0;
    // loop over all start nodes for linked lists in hash table
    for (int i = 0; i < BUCKETS+1; i++)
    {
        // traversal pointer
        node *cur = hashtable[i];
        // if dictionary is not yet loaded then move on to next bucket
        if (cur != NULL)
        {
            // traverse list and count number of words
            while (cur->next != NULL)
            {
                // check if there is a letter present in the word member of each node struct.
                // if there is then increment size variable, if not then move to next node.
                if (isalpha(cur->word[0]))
                {
                    size++;
                }
            cur = cur->next;
            }
            // if there is only one node, or it is the last node AND there is a letter in word
            // member of struct
            if (cur->next == NULL && isalpha(cur->word[0]))
            {
                size++;
            }
        }
    }
    return size;
}

// Unloads dictionary from memory, returning true if successful else false.
bool unload(void)
{
    // declare temporary pointer for this function
    node *ptr = NULL;
    // for each start node in hash table
    for (int i = 0; i < BUCKETS+1; i++)
    {
        // check if there is a node at that hash location
        if (hashtable[i] != NULL)
        {
            // delete nodes including last node
            while (hashtable[i]->next != NULL)
            {
                ptr = hashtable[i];
                hashtable[i] = ptr->next;
                free(ptr);
            }
            // if there is only one node, there will be no pointer to the next node
            if (hashtable[i]->next == NULL)
            {
                ptr = hashtable[i];
                free(ptr);
            }
        }
    }
    return true;
}

// hash function
int hash(const char *word)
{
    // convert and store first letter of word in variable (cant just use word because it is const)
    char letter = tolower(word[0]);
    // multiplication method (data structures text)
    int result = BUCKETS * (fmod((letter * 0.618033), 1));
    return result;
}