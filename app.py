from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from encryption import encrypt_file, decrypt_file, KEY_SIZE

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt')
def encrypt_page():
    return render_template('encrypt.html')

@app.route('/decrypt')
def decrypt_page():
    return render_template('decrypt.html')

@app.route('/upload/encrypt', methods=['POST'])
def upload_encrypt():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        key = os.urandom(KEY_SIZE)
        encrypted_file_path = encrypt_file(file_path, key)
        return f"File terenkripsi: {encrypted_file_path}, Kunci: {key.hex()}"

@app.route('/upload/decrypt', methods=['POST'])
def upload_decrypt():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    key = request.form['key']
    if file.filename == '':
        return "No selected file"
    if file and key:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        key = bytes.fromhex(key)
        decrypted_file_path = decrypt_file(file_path, key)
        return f"File terdekripsi: {decrypted_file_path}"

if __name__ == '__main__':
    app.run(debug=True)
