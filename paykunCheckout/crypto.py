import base64
import hashlib
import json
import os
from Crypto import Random
from Crypto.Cipher import AES
from phpserialize import loads, dumps
import hmac

class AESCipher():

    def __init__(self):
        self.key = b''

    def encrypt(self, string, key):
        self.key = key
        iv = os.urandom(16)
        string = dumps(string)
        padding = 16 - len(string) % 16
        # string += bytes(chr(padding) * padding)
        string += bytearray(chr(padding) * padding, 'utf8')
        value = base64.b64encode(self.mcrypt_encrypt(string, iv))
        iv = base64.b64encode(iv)
        mac = hmac.new(self.key, iv + value, hashlib.sha256).hexdigest()
        dic = {'iv': iv.decode(), 'value': value.decode(), 'mac': mac}
        return base64.b64encode(bytearray(json.dumps(dic),  'utf8'))

    def mcrypt_encrypt(self, value, iv):
        # AES.key_size = 128
        crypt_object = AES.new(self.key, AES.MODE_CBC, iv)
        return crypt_object.encrypt(value)
		