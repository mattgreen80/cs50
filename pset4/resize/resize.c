// Resizes a BMP file 

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: n copy infile outfile\n");
        return 1;
    }

    // remember filenames and store factor in variable
    char *infile = argv[2];
    char *outfile = argv[3];
    int fact = atoi(argv[1]);

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

/* -------Define two variables to store headers in, then read from infile's headers to the 
first variables (bf and bi) -------------------*/
    
    BITMAPFILEHEADER bf, bfout;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, biout;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // determine infile's padding for scanlines
    int paddingin = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
/* ---------create new headers for outfile ----------*/
    // copy the headers that were read from the infile into the outfile header variables created.
    bfout = bf;
    biout = bi;

    // edit width and height before writing to outfile
    biout.biWidth *= fact;
    biout.biHeight *= fact;
    
    // calculate padding for outfile
    int paddingout = (4 - (biout.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // edit image size before writing to outfile 
    biout.biSizeImage = ((sizeof(RGBTRIPLE) * biout.biWidth) + paddingout) * abs(biout.biHeight);
    bfout.bfSize = biout.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&bfout, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biout, sizeof(BITMAPINFOHEADER), 1, outptr);

/* ---- write the enlarged image to the outfile ----*/
    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // Make sure each row is written 'fact-1' number of times
        for (int m = 0; m < fact-1; m++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {   
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            
                // write RGB triple to outfile 'fact' number of times
                for (int k = 0; k < fact; k++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
                
            }
            // skip over infile's padding, if any
            fseek(inptr, paddingin, SEEK_CUR);
        
            // add padding to outfile
            for (int l = 0; l < paddingout; l++)
            {
                fputc(0x00, outptr);
            }        
            // send infile cursor back from the current position (end of scanline).
            fseek(inptr, -((sizeof(RGBTRIPLE) * bi.biWidth) + paddingin), SEEK_CUR);           
        } 
        // Write the row one more time without setting inptr's cursor back so that infile's scanline can increment
            for (int n = 0; n < bi.biWidth; n++)
            {   
                RGBTRIPLE triple;
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                for (int o = 0; o < fact; o++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }
            fseek(inptr, paddingin, SEEK_CUR);
            for (int l = 0; l < paddingout; l++)
            {
                fputc(0x00, outptr);
            }                
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
