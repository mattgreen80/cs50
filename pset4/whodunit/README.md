# Questions

## What's `stdint.h`?

This is a header file that provides typedefs for standardised integer types.  Part of the C99 standard.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

With C primitives the width can vary depending on the system they are compiled on, but the integer types specified above are of a fixed width.
This is useful for performing bitwise operations or any scenario where you need to work with a precise width integer.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1 byte, 4 bytes, 4 bytes and 2 bytes.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

0x4d42

## What's the difference between `bfSize` and `biSize`?

bfSize is the total size of the file including headers and padding, biSize is the size of the BITMAPINFOHEADER struct. 

## What does it mean if `biHeight` is negative?

This indicates that the .bmp is of the top-down type. This means that the image buffer is structured with the top image pixels first 
rather than the bottom-up type where they would be last in the buffer.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If the function fails to open a file it will return NULL instead of a pointer to the file it was attempting to open. 

## Why is the third argument to `fread` always `1` in our code?

Because we are reading only one element that is the size of a bitmap file header struct (i.e. we only want to read the header once).

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

padding will equal 3

## What does `fseek` do?

It is a function that takes the current file position, an offset in bytes and a position indicator and then changes the position 
within the file relative to the offset and position indicator. 

## What is `SEEK_CUR`?

This is a file position indicator that specifies the current position in the file. E.g used by fseek to specify that the 
offset will increment from the current position in the file rather than the start or end of the file. 
