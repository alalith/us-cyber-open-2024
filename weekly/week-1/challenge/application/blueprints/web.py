from flask import Blueprint, render_template, redirect, flash, current_app as app

web = Blueprint('web', __name__)


@web.route('/', methods=['GET'])
def updateView():
    return render_template('home.html')