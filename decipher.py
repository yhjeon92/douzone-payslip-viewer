#!/usr/bin/python3
import sys
import os
import base64
import hashlib
from bs4 import BeautifulSoup
from rc2_local import *


def decipher_from_string(view_data, password):
    arr = base64.b64decode(view_data)

    iv_bytes = arr[58:66]
    salt_bytes = arr[68:84]
    cipher_text = arr[88:]

    password_hash = sha1_hash(password.encode('utf-16le') + salt_bytes)
    key = password_hash[:16]

    ssn_decrypted = RC2(key).decrypt(cipher_text, MODE_CBC, IV=iv_bytes, padding=PADDING_PKCS5)
    result = ssn_decrypted.decode('utf-16le')

    return result


def parse_html(html_data):
    parsed = BeautifulSoup(html_data, features="lxml")
    view_data = parsed.find("input", {"name": "_viewData"}).get("value")
    view_data = view_data.strip()
    view_data = view_data.replace('\n', '')
    return view_data


def sha1_hash(data):
    hasher = hashlib.sha1()
    hasher.update(data)
    return hasher.digest()


def from_file(file_path, password):
    f = open(file_path, 'r')
    html_data = f.read()
    f.close()
    
    view_data = parse_html(html_data)
    return decipher_from_string(view_data, password)


def from_string(html_data, password):
    view_data = parse_html(html_data)
    return decipher_from_string(view_data, password)


if __name__ == '__main__':
    decrypted = from_file(sys.argv[1], sys.argv[2])

    f = open(os.getcwd() + '/decoded.html', 'w')
    f.write(decrypted)
    f.close()

