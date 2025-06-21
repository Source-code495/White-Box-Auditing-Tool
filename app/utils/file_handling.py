import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

Poss = {'png', 'jpg', 'jpeg', 'gif'}

def valid_model_file(file):
    """Check if uploaded file is a valid model file."""
    return file.filename != '' and file.filename.endswith(('.pth', '.pt'))

def create_session():
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(session_dir, exist_ok=True)
    return session_id, session_dir

def save_model(model_file, session_dir):
    filename = secure_filename(model_file.filename)
    model_path = os.path.join(session_dir, filename)
    model_file.save(model_path)
    return model_path

def save_uploaded_files(files, session_dir):
    saved_paths = []
    filenames = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(session_dir, filename)
            file.save(file_path)
            saved_paths.append(file_path)
            filenames.append(filename)
    return saved_paths, filenames

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Poss