from flask import jsonify, current_app as app
import base64
import json
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256, MD5
import io
import os
import tarfile
import logging

def response(message):
    return jsonify({'message': message})
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def downloadFirmware():

    K = open(app.config["PRIV_KEYPATH"],"r").read()
    R = RSA.import_key(K)

    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar:
        tar.add(app.config["FIRMWARE"], arcname="firmware.bin")

    firmware = base64.b64encode(tar_buffer.getvalue())

    H = SHA256.new(firmware)
    signer = PKCS115_SigScheme(R)
    signature = base64.b64encode(signer.sign(H))

    return json.dumps({"firmware":firmware.decode(),"signature":signature.decode()})

def unpackageFirmware(pkg):

    try:

        F = json.loads(pkg)

        Z = F.get("firmware",None)
        S = F.get("signature", None)

        if Z is None:
            return False, 'Invalid firmware package, missing TAR contents.'
        if S is None:
            return False, 'Invalid firmware package, missing signature.'

        tar_buffer = io.BytesIO(base64.b64decode(Z))

        folder = MD5.new(os.urandom(16)).hexdigest()
        filepath = os.path.join(app.config['FIRMWARE_FOLDER'],folder)

        K = open(app.config["PUB_KEYPATH"],"r").read()
        R = RSA.import_key(K)
        H = SHA256.new(Z.encode())
        S = base64.b64decode(S)

        verifier = PKCS115_SigScheme(R)
        try:
            verifier.verify(H, S)

            with tarfile.open(fileobj=tar_buffer,mode="r:gz") as TF:
                try:
                    TF.extractall(filepath)
                    return True, "Firmware package extracted to '%s'. Reboot device to finish firmware installation." % filepath
                except Exception as e:
                    logging.error(e)
                    return False, 'Invalid firmware package. Error extracting TAR contents.'
        except Exception as e:
            logging.error(e)
            return False, 'Invalid firmware package. Signature is invalid.'

    except Exception as e:
        logging.error(e)
        return False, 'Invalid firmware package. A decoding error occurred.'