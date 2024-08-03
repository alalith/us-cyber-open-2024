from flask import Blueprint, request, current_app as app, jsonify
from application.model import predict_image, validate_model
import os
import hashlib
import imghdr
import pathlib

api = Blueprint('api', __name__)


@api.route('/image/classify', methods=['POST'])
def api_classify_image():

    file = request.files.get("image")

    if not file or file.filename == "":
        return jsonify({"error":"No image provided."})
    
    # Random md5 sum for filename
    filename = hashlib.md5(os.urandom(16)).hexdigest()
    filepath = os.path.join(app.config['UPLOAD_DIR'],filename)
    file.save(filepath)

    # Check for valid image type
    if imghdr.what(filepath) not in ["png","jpeg"]:
        return jsonify({"error":"Invalid image provided. Please use PNG or JPG images."})

    result = jsonify(predict_image(filepath))

    # Clean things up
    os.unlink(filepath)

    return result

@api.route('/model/validate', methods=['POST'])
def api_validate_model():

    file = request.files.get("model")

    if not file or file.filename == "":
        return jsonify({"error":"No model provided."})
    
    ext = pathlib.Path(file.filename).suffix
    
    # Random md5 sum for filename
    filename = hashlib.md5(os.urandom(16)).hexdigest()
    filepath = os.path.join(app.config['UPLOAD_DIR'],filename+ext)
    file.save(filepath)

    result = jsonify(validate_model(filepath))

    # Clean things up
    os.unlink(filepath)

    return result
