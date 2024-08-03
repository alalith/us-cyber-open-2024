from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.PublicKey import RSA
import base64
import json
from Crypto.Hash import SHA256, MD5

K = open("private.pem","r").read()
R = RSA.import_key(K)

tar_file = open("custom_firmware.tar","rb").read()

firmware = base64.b64encode(tar_file)

H = SHA256.new(firmware)
signer = PKCS115_SigScheme(R)
signature = base64.b64encode(signer.sign(H))

print(json.dumps({"firmware":firmware.decode(),"signature":signature.decode()}))

