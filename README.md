# sercomm_fwutils_new
A set of utilites for manipulating Sercomm's router firmware images.

## Prerequisites
Python 3

After installing Python, run:
```
pip install cryptography
```
## Usage
For decompressing an image:
```
[-] Usage: python decompress_image.py <in_file> <out_file>
```
For decrypting an image:
```
[-] Usage: python decrypt_image.py <in_file> <out_file>
```

A required workflow is to first decompress an image and then decrypt it.
Once decrypted, you can feed the decrypted image to binwalk (to extract filesystem) like so:
```
binwalk -M -e decrypted_image.bin
```

## Tested firmware images
firmware-speedport-w724v-typc-v09011603-06-010.img
firmware-speedport-entry2-v090126-2-6-009-0.img
firmware-speedport-neo-v090128-2-6-008-0.img

## Inspiration
https://github.com/Psychotropos/sercomm_fwutils
