from flask import Blueprint, request, jsonify
import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


quantum_key_dist_api_bp = Blueprint("quantum_key_dist_api", __name__)

# configuring for key generation
KEY_SIZE = 32
SALT_SIZE = 16
BACKEND = default_backend()

#generating a new symmetric key
def generate_symmetric_key():
    salt = os.urandom(SALT_SIZE)
    kdf = Scrypt(salt=salt, length=KEY_SIZE, n=2**14, r=8, p=1, backend=BACKEND)
    key = kdf.derive(os.urandom(KEY_SIZE))
    return key, base64.b64encode(salt).decode() 

@quantum_key_dist_api_bp.route("/quantum_key_dist_api/get_key", methods=["GET"])
def get_key():
    try:
        key, salt = generate_symmetric_key()
        encoded_key = base64.b64encode(key).decode() #base 64 encode for JSON transmission
        #returning the key and salt as JSON
        return jsonify({
            "quantum_key":encoded_key,
            "salt":salt
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500
    

