// reveals a drawing

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 3)
    {
        fprintf(stderr, "Usage: infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];
    char *outfile = argv[2];

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

    /* read infile's BITMAPFILEHEADER. The fread function reads 1 element, the size of BITMAPFILEHEADER
    from the stream pointer (inptr) and stores it at the memory location pointed at by bf pointer. */
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
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

    // write outfile's BITMAPFILEHEADER. Write from address of bf the size of the BITMAPFILEHEADER To the outptr
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // iterate over infile's scanlines. abs funtion gives an absolute integer (why??).
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile stream
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            /* For each RGB value being read in the scan line, check if the pixel is pure red.
            If it is then change it to white */

            if (triple.rgbtRed == 0xff && triple.rgbtBlue == 0x00 && triple.rgbtGreen == 0x00)
            {
                triple.rgbtRed = 0xff;
                triple.rgbtBlue = 0xff;
                triple.rgbtGreen = 0xff;
            }
            
            // write RGB triple to outfile stream
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
        }

        // skip over padding, if any. This function seeks over the length of padding from the current position
        // (SEEK_CUR) in the input file (inptr).
        fseek(inptr, padding, SEEK_CUR);

        // then add it back (to demonstrate how). fput writes zeroes (as specified) to the outptr stream
        for (int k = 0; k < padding; k++)
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