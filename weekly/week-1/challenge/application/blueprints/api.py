from flask import Blueprint, request, redirect, flash, current_app as app, send_file
from application.util import unpackageFirmware, downloadFirmware
import hashlib
import os
import io

api = Blueprint('api', __name__)

@api.route('/firmware/upload', methods=['POST'])
def upload_firmware():

    file = request.files.get("file")

    if not file or file.filename == "":
        flash('You must select a file to upload.',"danger")
        return redirect("/")
    
    filename = hashlib.md5(os.urandom(16)).hexdigest()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    file.save(filepath)

    F = open(filepath,"r").read()

    ok, msg = unpackageFirmware(F)

    os.unlink(filepath)

    flash(msg,"success" if ok else "danger")
    return redirect("/")

@api.route('/firmware/download', methods=['GET'])
def download_firmware():

    firmware = downloadFirmware()
    buffer = io.BytesIO(firmware.encode())

    return send_file(buffer,mimetype="application/octet-stream",download_name="firmware.pkg",as_attachment=True)
