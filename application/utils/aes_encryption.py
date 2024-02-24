from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_aes(data, key):
    # Assuming `key` is defined; you might be passing this in a different way
    cipher = AES.new(key, AES.MODE_CBC)
    # Check if `data` is already a bytes object
    if isinstance(data, str):
        data = data.encode('utf-8')  # Encode string to bytes if it's not already bytes
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    return iv, ct_bytes

def decrypt_aes(enc_data, iv, key):
    # Assuming `key` is defined; you might be passing this in a different way
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(enc_data), AES.block_size)
    return pt
