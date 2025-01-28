from __future__ import annotations

import base64
import hashlib
import os
import random
import string

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from dotenv import load_dotenv


class Crypton:
    @staticmethod
    def generate_key(password, salt):
        """Derive a key from a password"""
        key = scrypt(password, salt, 32, N=2 ** 14, r=8, p=1)
        return key

    @staticmethod
    def encrypt_data(password, plaintext):
        """Encrypt data"""
        salt = get_random_bytes(16)
        key = Crypton.generate_key(password, salt)
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        encrypted, tag = cipher.encrypt_and_digest(plaintext.encode())
        return base64.urlsafe_b64encode(nonce + tag + salt + encrypted).decode('utf-8')

    @staticmethod
    def decrypt_data(password, ciphertext):
        """Decrypt data"""
        data = base64.urlsafe_b64decode(ciphertext)
        nonce = data[:16]
        tag = data[16:32]
        salt = data[32:48]
        encrypted = data[48:]
        key = Crypton.generate_key(password, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(encrypted, tag)
        return decrypted.decode('utf-8')

    @staticmethod
    def hash_sha256_data(data):
        """Returns a hexadecimal representation of the data hashed"""
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def get_envar(path: str, src: str, var_names: set | list | tuple) -> dict:
        """Get environment variables"""
        load_dotenv(os.path.join(path, src))
        return {varname: os.getenv(varname) for varname in var_names}

    @staticmethod
    def generate_secure_password(length=18):
        """Generate a strong password"""
        if length < 18:
            raise ValueError("Password length should be 18 characters or more")

        characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|:,.<>?/~"
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
