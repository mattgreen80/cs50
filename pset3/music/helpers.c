// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>
/* The quotes in the below directive statement indicate the header file is from your
own program rather than the system directories */
#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // Convert both numerator and denominator to an int and store in variables
    int n = atoi(&fraction[0]);
    int d = atoi(&fraction[2]);
    // If the denominator is 8 then just return the numerator because it is already an 8th
    if (d == 8)
    {
        return n;
    }
    // Else multiply by 2 until denominator equals 8 and then return numerator (which is now an 8th)
    else
    {
        while (d < 8)
        {
            n = n * 2;
            d = d * 2;
        }
        return n;
    }
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    /* The code below will calculate how far (in semitones) away the note given to the function 
    is from A4 and put it in the totaloffset variable. This value is required for the formula that 
    will calculate the frequency. A4 is the central point as specified by the formula. The totaloffset 
    variable is then given to the formula and the frequency of the note is calculated and returned 
    by the function. */

    // Initialise variables
    int noteoffset = 0;
    int accidentaloffset = 0;
    int octaveoffset = 0;
    char octave;
    float totaloffset;
    float freq;
    
    
    // First check if the value is A4. 440 is the frequency of A4 in Hertz.
    if (note[0] == 'A' && note[1] == '4')
    {
        return 440;
    }
    
    // If there are any accidentals present in the string, include them in the total offset calculation.
    // Also put the octave into a variable because its position in the array changes depending on the presence of an accidental.
    if (note[1] == '#')
    {
        octave = note[2];
        accidentaloffset = 1;
    } 
    else if (note[1] == 'b')
    {
        octave = note[2];
        accidentaloffset = -1;
    }
    else
    {
        octave = note[1];
    }
    // Switch statement to calculate ocatave offset from 4 (8 octaves total). 
    switch(octave) 
    {
    case '4' :
        break;
    case '5' :
        octaveoffset = 1;
        break;
    case '6' :
        octaveoffset = 2;
        break;
    case '7' :
        octaveoffset = 3;
        break;
    case '8' :
        octaveoffset = 4;
        break;
    case '0' :
        octaveoffset = -4;
        break;
    case '1' :
        octaveoffset = -3;
        break;
    case '2' :
        octaveoffset = -2;
        break;
    case '3' :
        octaveoffset = -1;
    default :
        break;
    }
    
    // Switch statement to calculate semitone offset from A which is equal to 0 (11 semitones total from note C to B)
    switch(note[0]) 
    {
    case 'A' :
        break;
    case 'B' :
        noteoffset = 2;
        break;
    case 'C' :
        noteoffset = -9;
        break;
    case 'D' :
        noteoffset = -7;
        break;
    case 'E' :
        noteoffset = -5;
        break;
    case 'F':
        noteoffset = -4;
        break;
    case 'G':
        noteoffset = -2;
        break;
    default :
        break;
    }  
    // Formula to calculate total offset
    totaloffset = 12*octaveoffset + noteoffset + accidentaloffset;
    // Formula to calculate the frequency of the input note and return.
    freq = roundf((powf(2, totaloffset/12.0)*440));
    return freq;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    // If the first char in the string array is blank then return true; If not then return false.
    if (strcmp (&s[0], "") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
