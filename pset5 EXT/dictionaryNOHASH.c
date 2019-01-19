// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#include "dictionary.h"


// global pointer to the start of the linked list
node *start = NULL;


// Returns true if word is in dictionary else false. NOT WORKING
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
    // pointer to start node
    node *cur = start;
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
            temp->next = start;
            // now change the new nodes pointer to make it the new first node
            start = temp;
    }
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded. 
unsigned int size(void)
{
    // traversal pointer
    node *cur = start;
    // if dictionary is not yet loaded (no pointer to first node)
    if (cur == NULL)
    {
        return 0;
    }
    // keep track of words
    int size = 1;
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
    return size;
}

// Unloads dictionary from memory, returning true if successful else false. 
bool unload(void)
{
    // declare temporary pointer for this function
    node *ptr = NULL;
    // check if there is a node at all
    if (start == NULL)
    {
        return false;
    }
    // delete nodes including last node
    while (start->next != NULL)
    {
        ptr = start;
        start = ptr->next;
        free(ptr);
    }
    // if there is only one node, there will be no pointer to the next node
    if (start->next == NULL)
    {
        ptr = start;
        free(ptr);
    }
    return true;
}

// hash function
int hash(int key)
{
    // multiplication method (data structures text)
    int result = 200 * (key * fmod(0.618033, 1));
    return result;
}