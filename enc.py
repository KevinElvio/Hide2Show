import os
import struct
import argparse

# Constants for ChaCha20
CHACHA20_KEY_SIZE = 32
CHACHA20_NONCE_SIZE = 12
CHACHA20_BLOCK_SIZE = 64
CHACHA20_ROUNDS = 20

# ChaCha20 quarter round
def quarter_round(x, a, b, c, d):
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = x[d] ^ x[a]
    x[d] = ((x[d] << 16) & 0xffffffff) | (x[d] >> (32 - 16))
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = x[b] ^ x[c]
    x[b] = ((x[b] << 12) & 0xffffffff) | (x[b] >> (32 - 12))
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = x[d] ^ x[a]
    x[d] = ((x[d] << 8) & 0xffffffff) | (x[d] >> (32 - 8))
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = x[b] ^ x[c]
    x[b] = ((x[b] << 7) & 0xffffffff) | (x[b] >> (32 - 7))

# ChaCha20 block function
def chacha20_block(key, counter, nonce):
    constants = b'expand 32-byte k'
    state = [
        struct.unpack('<I', constants[0:4])[0],
        struct.unpack('<I', constants[4:8])[0],
        struct.unpack('<I', constants[8:12])[0],
        struct.unpack('<I', constants[12:16])[0],
        struct.unpack('<I', key[0:4])[0],
        struct.unpack('<I', key[4:8])[0],
        struct.unpack('<I', key[8:12])[0],
        struct.unpack('<I', key[12:16])[0],
        struct.unpack('<I', key[16:20])[0],
        struct.unpack('<I', key[20:24])[0],
        struct.unpack('<I', key[24:28])[0],
        struct.unpack('<I', key[28:32])[0],
        counter,
        struct.unpack('<I', nonce[0:4])[0],
        struct.unpack('<I', nonce[4:8])[0],
        struct.unpack('<I', nonce[8:12])[0]
    ]

    working_state = state[:]
    for _ in range(CHACHA20_ROUNDS // 2):
        quarter_round(working_state, 0, 4, 8, 12)
        quarter_round(working_state, 1, 5, 9, 13)
        quarter_round(working_state, 2, 6, 10, 14)
        quarter_round(working_state, 3, 7, 11, 15)
        quarter_round(working_state, 0, 5, 10, 15)
        quarter_round(working_state, 1, 6, 11, 12)
        quarter_round(working_state, 2, 7, 8, 13)
        quarter_round(working_state, 3, 4, 9, 14)

    return b''.join(struct.pack('<I', (working_state[i] + state[i]) & 0xffffffff) for i in range(16))

# ChaCha20 encryption
def chacha20_encrypt(key, nonce, plaintext):
    counter = 0
    ciphertext = bytearray(plaintext)
    for i in range(0, len(plaintext), CHACHA20_BLOCK_SIZE):
        key_stream = chacha20_block(key, counter, nonce)
        counter += 1
        for j in range(min(len(plaintext) - i, CHACHA20_BLOCK_SIZE)):
            ciphertext[i + j] ^= key_stream[j]
    return bytes(ciphertext)

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as f:
        plaintext = f.read()

    if len(plaintext) == 0:
        raise ValueError("File is empty")

    nonce = os.urandom(CHACHA20_NONCE_SIZE)
    ciphertext = nonce + chacha20_encrypt(key, nonce, plaintext)

    encrypted_file = file_name + '.enc'
    with open(encrypted_file, 'wb') as f:
        f.write(ciphertext)
    
    return encrypted_file

def main():
    parser = argparse.ArgumentParser(description="Enkripsi file menggunakan ChaCha20.")
    parser.add_argument('operation', help="Operasi yang ingin dilakukan: encrypt.")
    parser.add_argument('filename', help="Nama file yang akan dienkripsi.")
    args = parser.parse_args()

    if args.operation == 'encrypt':
        key = os.urandom(CHACHA20_KEY_SIZE)
        try:
            encrypted_file = encrypt_file(args.filename, key)
            print(f"File terenkripsi: {encrypted_file}")
            print(f"Kunci enkripsi: {key.hex()}")
        except ValueError as e:
            print(e)
    else:
        print("Operasi tidak dikenal. Gunakan 'encrypt'.")

if __name__ == "__main__":
    main()


import os
import struct
import argparse

# Constants for ChaCha20
CHACHA20_KEY_SIZE = 32
CHACHA20_NONCE_SIZE = 12
CHACHA20_BLOCK_SIZE = 64
CHACHA20_ROUNDS = 20

# ChaCha20 quarter round
def quarter_round(x, a, b, c, d):
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = x[d] ^ x[a]
    x[d] = ((x[d] << 16) & 0xffffffff) | (x[d] >> (32 - 16))
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = x[b] ^ x[c]
    x[b] = ((x[b] << 12) & 0xffffffff) | (x[b] >> (32 - 12))
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = x[d] ^ x[a]
    x[d] = ((x[d] << 8) & 0xffffffff) | (x[d] >> (32 - 8))
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = x[b] ^ x[c]
    x[b] = ((x[b] << 7) & 0xffffffff) | (x[b] >> (32 - 7))

# ChaCha20 block function
def chacha20_block(key, counter, nonce):
    constants = b'expand 32-byte k'
    state = [
        struct.unpack('<I', constants[0:4])[0],
        struct.unpack('<I', constants[4:8])[0],
        struct.unpack('<I', constants[8:12])[0],
        struct.unpack('<I', constants[12:16])[0],
        struct.unpack('<I', key[0:4])[0],
        struct.unpack('<I', key[4:8])[0],
        struct.unpack('<I', key[8:12])[0],
        struct.unpack('<I', key[12:16])[0],
        struct.unpack('<I', key[16:20])[0],
        struct.unpack('<I', key[20:24])[0],
        struct.unpack('<I', key[24:28])[0],
        struct.unpack('<I', key[28:32])[0],
        counter,
        struct.unpack('<I', nonce[0:4])[0],
        struct.unpack('<I', nonce[4:8])[0],
        struct.unpack('<I', nonce[8:12])[0]
    ]

    working_state = state[:]
    for _ in range(CHACHA20_ROUNDS // 2):
        quarter_round(working_state, 0, 4, 8, 12)
        quarter_round(working_state, 1, 5, 9, 13)
        quarter_round(working_state, 2, 6, 10, 14)
        quarter_round(working_state, 3, 7, 11, 15)
        quarter_round(working_state, 0, 5, 10, 15)
        quarter_round(working_state, 1, 6, 11, 12)
        quarter_round(working_state, 2, 7, 8, 13)
        quarter_round(working_state, 3, 4, 9, 14)

    return b''.join(struct.pack('<I', (working_state[i] + state[i]) & 0xffffffff) for i in range(16))

# ChaCha20 encryption/decryption
def chacha20_encrypt_decrypt(key, nonce, data):
    counter = 0
    result = bytearray(data)
    for i in range(0, len(data), CHACHA20_BLOCK_SIZE):
        key_stream = chacha20_block(key, counter, nonce)
        counter += 1
        for j in range(min(len(data) - i, CHACHA20_BLOCK_SIZE)):
            result[i + j] ^= key_stream[j]
    return bytes(result)

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as f:
        plaintext = f.read()

    if len(plaintext) == 0:
        raise ValueError("File is empty")

    nonce = os.urandom(CHACHA20_NONCE_SIZE)
    ciphertext = nonce + chacha20_encrypt_decrypt(key, nonce, plaintext)

    encrypted_file = file_name + '.enc'
    with open(encrypted_file, 'wb') as f:
        f.write(ciphertext)
    
    return encrypted_file

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as f:
        data = f.read()

    if len(data) <= CHACHA20_NONCE_SIZE:
        raise ValueError("File is too short to contain a valid nonce")

    nonce = data[:CHACHA20_NONCE_SIZE]
    ciphertext = data[CHACHA20_NONCE_SIZE:]
    plaintext = chacha20_encrypt_decrypt(key, nonce, ciphertext)

    decrypted_file = file_name[:-4]  # remove the '.enc' extension
    with open(decrypted_file, 'wb') as f:
        f.write(plaintext)
    
    return decrypted_file

def main():
    parser = argparse.ArgumentParser(description="Enkripsi dan dekripsi file menggunakan ChaCha20.")
    parser.add_argument('operation', help="Operasi yang ingin dilakukan: encrypt atau decrypt.")
    parser.add_argument('filename', help="Nama file yang akan dienkripsi atau didekripsi.")
    parser.add_argument('--key', help="Kunci enkripsi/dekripsi dalam format hex (untuk dekripsi).")
    args = parser.parse_args()

    if args.operation == 'encrypt':
        key = os.urandom(CHACHA20_KEY_SIZE)
        try:
            encrypted_file = encrypt_file(args.filename, key)
            print(f"File terenkripsi: {encrypted_file}")
            print(f"Kunci enkripsi: {key.hex()}")
        except ValueError as e:
            print(e)
    elif args.operation == 'decrypt':
        if not args.key:
            print("Kunci enkripsi diperlukan untuk dekripsi.")
            return
        key = bytes.fromhex(args.key)
        try:
            decrypted_file = decrypt_file(args.filename, key)
            print(f"File terdekripsi: {decrypted_file}")
        except ValueError as e:
            print(e)
    else:
        print("Operasi tidak dikenal. Gunakan 'encrypt' atau 'decrypt'.")

if __name__ == "__main__":
    main()
