import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from hsmt.models import *

class AESCipher(object):
    '''Implement AES cipher for unicode key and plaintext'''

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = raw.encode('utf-8')
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode('utf-8')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def encode(raw, key):
    if raw == '':
        return raw
    encoder = AESCipher(key)
    return encoder.encrypt(raw).decode('utf-8')

def decode(cipher, key):
    if cipher == '':
        return cipher
    decoder = AESCipher(key)
    return decoder.decrypt(cipher.encode('utf-8'))

def encode_for_object(obj, key):
    if isinstance(obj, XFile):
        secret_content = json.loads(obj.content)
        for record_name in secret_content.keys():
            record = secret_content[record_name]
            record['value'] = encode(record['value'], key)
        obj.content = json.dumps(secret_content)
    elif isinstance(obj, AttackLog):
        obj.result = encode(obj.result, key)
        obj.process = encode(obj.process, key)
    elif isinstance(obj, XFileChange):
        secret_content = json.loads(obj.content)
        for record_name in secret_content.keys():
            record = secret_content[record_name]
            record['new'] = encode(record['new'], key)
            record['old'] = encode(record['old'], key)
        obj.content = json.dumps(secret_content)
    else:
        raise Exception('Unexpected type of object')
    return obj

def decode_for_object(obj, key):
    if isinstance(obj, XFile):
        secret_content = json.loads(obj.content)
        for record_name in secret_content.keys():
            record = secret_content[record_name]
            record['value'] = decode(record['value'], key)
        obj.content = json.dumps(secret_content)
    elif isinstance(obj, AttackLog):
        obj.result = decode(obj.result, key)
        obj.process = decode(obj.process, key)
    elif isinstance(obj, XFileChange):
        secret_content = json.loads(obj.content)
        for record_name in secret_content.keys():
            record = secret_content[record_name]
            record['new'] = decode(record['new'], key)
            record['old'] = decode(record['old'], key)
        obj.content = json.dumps(secret_content)
    else:
        raise Exception('Unexpected type of object')
    return obj

def encode_for_department(department_id, key):
    list_xfile = set(XFile.objects.filter(department__id=department_id))
    list_attacklog = set()
    list_changes = set()
    for xfile in list_xfile:
        attacklogs = set(xfile.attack_logs.all())
        changes = set(xfile.changes.all())
        list_attacklog.update(attacklogs)
        list_changes.update(changes)
    # Encode everything
    for xfile in list_xfile:
        encode_for_object(xfile, key).save()
    for attacklog in list_attacklog:
        encode_for_object(attacklog, key).save()
    for change in list_changes:
        encode_for_object(change, key).save()

def decode_for_department(department_id, key):
    list_xfile = set(XFile.objects.filter(department__id=department_id))
    list_attacklog = set()
    list_changes = set()
    for xfile in list_xfile:
        attacklogs = set(xfile.attack_logs.all())
        changes = set(xfile.changes.all())
        list_attacklog.update(attacklogs)
        list_changes.update(changes)
    # Decode everything
    for xfile in list_xfile:
        decode_for_object(xfile, key).save()
    for attacklog in list_attacklog:
        decode_for_object(attacklog, key).save()
    for change in list_changes:
        decode_for_object(change, key).save()

def update_pwd_for_xfile_department(department_id, password_old, password_new):
    decode_for_department(department_id, password_old)
    encode_for_department(department_id, password_new)

if __name__ == '__main__':
    # raw = 'Đỗ Bảo Hoàng'
    # key = 'phòng 123'
    # cipher = encode(raw, key)
    # decoded_cipher = decode(cipher, key)
    # print('cipher', cipher)
    # print('raw', decoded_cipher)

    # xfile = XFile.objects.first()
    # print(xfile.content)
    # encoded_xfile = encode_for_object(xfile, 'abcde')
    # print(encoded_xfile.content)
    pass