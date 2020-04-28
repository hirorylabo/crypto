#!/usr/bin/env python3
# coding: utf-8
import secrets
import ecdsa
import hashlib
import base58
import time
# import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText

# range = range(10**10)
range = range(1000)

with open("richlist_v1.5.csv") as fp:
    data = set(fp.read().splitlines())
    # data = fp.read().splitlines()


class Generater():
    def __init__(self):
        # p = 2**256-2**32-2**9-2**8-2**7-2**6-2**4-1
        p = 4294967296
        privkey = self.new_privkey(p)
        pubkey = self.new_pubkey(privkey)
        address = self.new_address(bytes.fromhex("00"), pubkey)
        # テスト用
        # address = "15xRtvr7kmWYVG79oi9EHF8s7VF7RZx4V7"
        # テスト
        self.value = []
        self.value.append(address)
        self.value.append(privkey)

    def new_privkey(self, p):
        privkey = secrets.randbelow(p)
        privkey = format(privkey, 'x').zfill(64)
        return privkey

    def new_pubkey(self, privkey):
        bin_privkey = bytes.fromhex(privkey)
        signing_key = ecdsa.SigningKey.from_string(
            bin_privkey, curve=ecdsa.SECP256k1)
        verifying_key = signing_key.get_verifying_key()
        pubkey = bytes.fromhex("04") + verifying_key.to_string()
        pubkey = pubkey.hex()
        # print("PublicKey = " + pubkey)
        return pubkey

    def new_address(self, version, pubkey):
        ba = bytes.fromhex(pubkey)
        digest = hashlib.sha256(ba).digest()
        new_digest = hashlib.new('ripemd160')
        new_digest.update(digest)
        pubkey_hash = new_digest.digest()

        pre_address = version + pubkey_hash
        address = hashlib.sha256(pre_address).digest()
        address = hashlib.sha256(address).digest()
        checksum = address[:4]
        address = pre_address + checksum
        address = base58.b58encode(address)
        address = address.decode()
        # print("Address = " + address + "\n")
        return address


t1 = time.time()


for i in range:
    # print(i)
    keydata = Generater().value
    # print(keydata)
    address = keydata[0]
    privkey = keydata[1]

    if address in data:
        # SMTP認証情報
        account = "bitlabo001@gmail.com"
        password = "haif.BOOX5mul!red"
        # 送受信先
        to_email = "penya.shk@gmail.com"
        from_email = "bitlabo001@gmail.com"
        # MIMEの作成
        subject = "ラボマイニングジャックポット！！"
        message = address + "\n" + "\n" + privkey
        msg = MIMEText(message, "html")
        msg["Subject"] = subject
        msg["To"] = to_email
        msg["From"] = from_email
        server = smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=ssl.create_default_context())
        server.login(account, password)
        server.send_message(msg)
        server.quit()
        break

t2 = time.time()

elapsed_time = t2-t1
print(elapsed_time)
