from flask import Blueprint, request, jsonify, session
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
from flask_login import login_required, current_user
from flask_socketio import emit
from src.authentication_app.models import User
from src.authentication_app.views import auth_status

communication_app_bp = Blueprint("communication_app", __name__)

QKD_API_URL = "http://127.0.0.1:5000/quantum_key_dist_api/get_key"

#function to retrieve a secure quantum key from the QKD api
def get_quantum_key():
    response = requests.get(QKD_API_URL)
    if response.status_code == 200:
        key = base64.b64decode(response.json().get("quantum_key")) # Assume the key is base64 encoded
        return key
    else:
        raise Exception("Failed to obtain quantum key")

# AES-GCM encryptiom
def encrypt_data(data, key):
    iv = os.urandom(12) # 12-byte IV for AES-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()

    return {
        "iv":base64.b64encode(iv).decode(),
        "cipher_text":base64.b64encode(encrypted_data).decode(),
        "tag":base64.b64encode(encryptor.tag).decode(),
        "quantum_key":base64.b64encode(key).decode()
    }

#AES-GCM decryption
def decrypt_data(encrypted_data, key, iv, tag):
    iv = base64.b64decode(iv)
    tag = base64.b64decode(tag)
    encrypted_data = base64.b64decode(encrypted_data)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data.decode()

#Route to initialize communication and fetch a quantum key
@communication_app_bp.route("/api/communication/initialize", methods=["GET"])
def initialize():
    """
    everytime if this route is called a new quantum key is generated
    """
    try:
        if not auth_status.get("user_public_id"):
            return jsonify({"status":"Unauthorized"}), 401
        quantum_key = get_quantum_key()
        return jsonify({"status":"Initailized", "quantum_key":base64.b64encode(quantum_key).decode()})
    except Exception as e:
        return jsonify({"error":str(e)}), 500

#endpoint to send encrypted_data
@communication_app_bp.route("/api/communication/send_data", methods=["POST"])
def send_data():
    """
    this route is for sending encrypted data
    post request with json data
    Keys: data, quantum_key
    """
    try:
        if not auth_status.get("user_public_id"):
            return jsonify({"status":"Unauthorized"}), 401
        data = request.json.get("data")
        quantum_key = base64.b64decode(request.json.get("quantum_key")) #decode the base64 key
        #encrypting the data
        encrypted = encrypt_data(data, quantum_key)
        #return encrypted data (iv, ciphertext, tag) for communication
        return jsonify(encrypted)
    except Exception as e:
        return jsonify({"error":str(e)}), 500

#endpoint to receive encrypted data and decrypt it
@communication_app_bp.route("/api/communication/receive_data", methods=["POST"])
def receive_data():
    """
    After sending the data the send_data route returns the 'iv', 'tag', and 'ciphertext'
    for decryting the data you need to call this route and pass the 'iv', 'tag', 'cipher_text' and 'quantum_key'
    """
    try:
        if not auth_status.get("user_public_id"):
            return jsonify({"status":"Unauthorized"}), 401
        data = request.json.get("datas")
        encrypted_data = data.get("cipher_text")
        iv = data.get("iv")
        tag = data.get("tag")
        quantum_key = base64.b64decode(data.get("quantum_key")) # decode the base64 key
        #decrypt the data
        decrypted_data = decrypt_data(encrypted_data, quantum_key, iv, tag)

        return jsonify({"decrypted_data":decrypted_data})
    except Exception as e:
        return jsonify({"error":str(e)}), 500