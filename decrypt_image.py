import os
import sys
import hashlib
import struct
import string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class LimitedFileWriter:
    def __init__(self, filename, max_size):
        self.filename = filename
        self.max_size = max_size
        self.file = open(filename, 'wb')

    def write(self, data):
        if self.file.tell() + len(data) <= self.max_size:
            self.file.write(data)
        else:
            self.file.write(data[0:(self.max_size - self.file.tell())])
        return True

    def close(self):
        self.file.close()

def get_data_slice(data, offset):
    return data[offset:offset+32]

def get_md5(data, key1, key2, key3):
    md5 = hashlib.md5()

    md5.update(key1)
    md5.update(key3)
    digest1 = md5.digest()
    
    md5 = hashlib.md5()
    md5.update(key2)
    md5.update(key3)
    digest2 = md5.digest()
    
    out = b''
    for digest in (digest1, digest2):
        out += struct.pack('<IIII', *struct.unpack('<IIII', digest))
    
    return out
    
def convert_to_bytes(input):
    output = bytes()
    
    for elem in input:
        output += bytes([(elem & 0xff)])
    
    return output
    
def fw_decrypt(infile, output_file, key, iv, decrypted_size):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    writer = LimitedFileWriter(output_file, decrypted_size)

    decryptor = cipher.decryptor()
    while True:
        chunk = infile.read(1024)
        if not chunk:
            break
        decrypted_chunk = decryptor.update(chunk)
        writer.write(decrypted_chunk)
    decrypted_final = decryptor.finalize()
    writer.write(decrypted_final)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('[-] Usage: python decrypt_image.py <in_file> <out_file>')
        sys.exit(1)
        
    input_file, output_file = sys.argv[1:]

    with open(input_file, 'rb') as infile:
        try:
            input_data = infile.read(0xa0)
            
            key1 = get_data_slice(input_data, 96)
            key2 = get_data_slice(input_data, 128)
            key3 = get_data_slice(input_data, 32)
            
            key = get_md5(input_data, key1, key2, key3)
            iv = input_data[64:64+16]
            decrypted_size = int(bytes(input_data[128:128+16]).strip(b"\0"))
            fw_decrypt(infile, output_file, convert_to_bytes(key), iv, decrypted_size)
            print('[o] Successfully decrypted.')
        except Exception as e:
            print('[x] An error occurred: ', e)  
            sys.exit(2)
        