# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

It is the longest word in the english language and a synonym for Silicosis, a lung disease caused by inhalation of Silica dust.

## According to its man page, what does `getrusage` do?

Returns resource usage for SELF(total process resources) CHILDREN (only child processes of the calling process) or THREAD (just the calling thread) 
in the form of a struct called rusage. 

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

So that the function does not have to copy the contents of the structs into stack memory (call by value). This would take more time and use more memory. 

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

The for loop initialises the variable c with a call to fget that converts the char in the stream to an int. The loop will run 
iterating over each char in the file until the c variable equals EOF.
If the c variable is an ASCII letter or an apostrophe among letters in a word, then the c variable is put at its corresponding location
(index) in the word buffer and then the index is incremented ready for the next letter. If the word becomes longer than the maximum 
length then keep iterating over the remaining characters of that word and reset the index of the current word back to zero.
If the current character in the word is instead a digit, then continue to iterate over the rest of the string and set the word index to zero 
ready for the next word. By now, if the word index is not equal to zero and we have not already found a character, then we must have a word. 
Thus, add a terminating char to the string and increment the word counter. We now check if the word was mispelled by passing the word buffer to the 
check function (while also checking how long this takes). If the mispelled boolean is true then we print the word to stdout and take note that there 
was a word mispelled by incrementing the counter. Then finally, we reset the word index ready for the next word and the loop starts again. 


## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

Because with fscanf, we cannot check if the word contained a numeric digit or if the word is too long, we only know that it is a string. 

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

So the name of the dictionary or word passed to the function cannot be modified by the function (i.e. the value passed is read only).
