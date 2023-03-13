from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
import os
import base64

class AESkey:
    def __init__(self):
        self.key = b'\xf1z\xc0E\x7f\xb6\xac\xbeJ=\xfcb\xfar\xa4\xd6\xb8\xd4\x18o\xe5q\xfb\x97"k\xa0\xb4J\x8c\x84\xae'
        
    def share_AESkey(self):
       os.environ['AESkey'] = base64.b64encode(self.key).decode('utf-8')
           

object_Aeskey = AESkey()
object_Aeskey.share_AESkey()
