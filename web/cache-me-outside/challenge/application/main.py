from flask import Flask, request, jsonify, session, render_template, send_file, redirect
from redis import Redis
from functools import wraps
from logging.config import dictConfig
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
import random
import string
import re
import threading

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config.from_object('application.config.Config')

redis = Redis(host=app.config.get("REDIS_HOST"), port=6379, db=0)
lock = threading.Lock()

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/dashboard', methods=['GET'])
def dashboard():

    if not session.get("logged_in",False):
        return redirect("/")
    
    return render_template("dashboard.html",role=session["role"],FLAG=os.getenv("FLAG"))

@app.route('/logout', methods=['GET'])
def logout():
    session["logged_in"] = False
    del(session["role"])
    del(session["username"])
    return redirect("/")

@app.route('/api/register', methods=['POST'])
def register():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing parameters"}), 400
    
    with lock:

        if redis.exists(f"user:{username}:password"):
            return jsonify({"error": "Username already exists"}), 400
        
        redis.set(f"user:{username}:role", "unverified")
        redis.set(f"user:{username}:password", generate_password_hash(password))
        
        # Make sure that username isn't in password, for security reasons
        matches = re.match(username,password)

        if matches:
            redis.delete(f"user:{username}:role")
            redis.delete(f"user:{username}:password")
            return jsonify({"error": "Username can't be in password."}), 400
        
        if username != "admin":
            redis.set(f"user:{username}:role", "user")

        return jsonify({"message": "User registered successfully"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing parameters"}), 400

    stored_password = redis.get(f"user:{username}:password")

    if not stored_password:
        return jsonify({"error": "Invalid username or password"}), 403

    if check_password_hash(stored_password.decode(),password):
        session["logged_in"] = True
        session['username'] = username
        session['role'] = redis.get(f"user:{username}:role").decode()
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 403

@app.route('/favicon.ico',methods=['GET'])
def icon():
    return send_file("static/favicon.ico")