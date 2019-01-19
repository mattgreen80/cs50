/* Reads a card image and outputs the JPEG files found within */

#include <stdio.h>
#include <stdlib.h>
// add further int types
#include <stdint.h>


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // remember filename
    char *img = argv[1];

    // open image file
    FILE *imgptr = fopen(img, "r");
    if (imgptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", img);
        return 2;
    }
// Allocate memory for fread to use
    uint8_t *buffer = malloc(512 * sizeof(uint8_t));
// char array for output jpg file names
    char filename[8];
// count for file names
    int count = 0;
// define file pointer so it can be manipulated outside of local statements
    FILE *imgout = NULL;
// fread 512 blocks in from imgptr. loop until fread returns no number which means EOF
    while (fread(buffer, 512, 1, imgptr) > 0)
    {
        // check if first bytes match JPG signature (if statement with 
        // bitwise AND at the end) If true then write JPG.
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // if first jpeg then write to new file. Use file name count to test if first JPG.
            if (count == 0)
            {
                // print new file name to array
                sprintf(filename, "%03i.jpg", count);
                // increment file name count 
                count++;
                // open new JPG file
                imgout = fopen(filename, "w");
                // write JPG to new file. put in loop??
                fwrite(buffer, 512, 1, imgout);
            }
            // if not first jpeg then close previous file before writing to new file. 
            else
            {
                // close previous image file
                fclose(imgout);
                // print new file name to array
                sprintf(filename, "%03i.jpg", count);
                // increment file name count 
                count++;
                // open new JPG file
                imgout = fopen(filename, "w");
                // write JPG to new file. 
                fwrite(buffer, 512, 1, imgout);
            }
        }
        // if the 512 is not the start of a JPG
        else
        {
            // if file name count is greater than 0 then it must be part of a JPG so write it. 
            // else count must be 0 so loop back and read a new 512 to find a JPG.
            if (count > 0) 
            {
                // write 512 to the image file
                fwrite(buffer, 512, 1, imgout);
            }
        }
    }
    // close infile
    fclose(imgptr);
    // close last jpg 
    fclose(imgout);
    // free memory
    free(buffer);
    // success
    return 0;
}