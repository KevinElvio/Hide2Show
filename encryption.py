import os
import struct

# Constants for encryption
KEY_SIZE = 32
NONCE_SIZE = 12
BLOCK_SIZE = 64
ROUNDS = 20

def simple_quarter_round(x, a, b, c, d):
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

def simple_block(key, counter, nonce):
    constants = (0x61707865, 0x3320646e, 0x79622d32, 0x6b206574)
    key_state = struct.unpack('<8I', key)
    counter_state = (counter,)
    nonce_state = struct.unpack('<3I', nonce)
    state = list(constants + key_state + counter_state + nonce_state)
    working_state = list(state)

    for _ in range(ROUNDS // 2):
        simple_quarter_round(working_state, 0, 4, 8, 12)
        simple_quarter_round(working_state, 1, 5, 9, 13)
        simple_quarter_round(working_state, 2, 6, 10, 14)
        simple_quarter_round(working_state, 3, 7, 11, 15)
        simple_quarter_round(working_state, 0, 5, 10, 15)
        simple_quarter_round(working_state, 1, 6, 11, 12)
        simple_quarter_round(working_state, 2, 7, 8, 13)
        simple_quarter_round(working_state, 3, 4, 9, 14)

    output = bytearray()
    for i in range(16):
        output += struct.pack('<I', (working_state[i] + state[i]) & 0xffffffff)

    return bytes(output)

def simple_encrypt(key, counter, nonce, plaintext):
    encrypted = bytearray()
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = simple_block(key, counter, nonce)
        chunk = plaintext[i:i + BLOCK_SIZE]
        encrypted += bytes(a ^ b for a, b in zip(chunk, block))
        counter += 1
    return encrypted

def simple_decrypt(key, counter, nonce, ciphertext):
    return simple_encrypt(key, counter, nonce, ciphertext)  # Symmetric encryption

def encrypt_file(file_path, key):
    nonce = os.urandom(NONCE_SIZE)
    counter = 1

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = simple_encrypt(key, counter, nonce, plaintext)
    encrypted_file_path = file_path + '.enc'
    
    with open(encrypted_file_path, 'wb') as f:
        f.write(nonce + ciphertext)
    
    return encrypted_file_path

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        nonce = f.read(NONCE_SIZE)
        ciphertext = f.read()

    counter = 1
    plaintext = simple_decrypt(key, counter, nonce, ciphertext)
    decrypted_file_path = file_path + '.dec'
    
    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)
    
    return decrypted_file_path
