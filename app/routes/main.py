from flask import Blueprint, render_template, current_app
from app.utils.file_handling import allowed_file

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')