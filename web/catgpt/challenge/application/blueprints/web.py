from flask import Blueprint, render_template, send_file

web = Blueprint('web', __name__)

@web.route('/', methods=['GET'])
def indexView():
    return render_template('index.html')

@web.route('/contribute', methods=['GET'])
def contributeView():
    return render_template('contribute.html')


@web.route('/model', methods=['GET'])
def modelView():
    return send_file("model/base_model.h5")