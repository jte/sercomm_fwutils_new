import gzip
import sys

def decompress_fw(infile, outfile):
    infile.seek(0xa0)
    with gzip.open(infile, "rb") as gf:
        decompressed = bytearray(0xa0)
        while gf.readinto(decompressed) == 0xa0:
            outfile.write(decompressed)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('[-] Usage: python decompress_image.py <in_file> <out_file>')
        sys.exit(1)
    
    input_file, output_file = sys.argv[1:]
    
    with open(output_file, "wb") as dout, open(input_file, "rb") as fwin: 
        try:
            decompress_fw(fwin, dout)
            print('[o] Successfully decompressed.')
        except Exception as e:
            print('[x] An error occurred: ', e)  
            sys.exit(2)