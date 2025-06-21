from flask import Flask, send_from_directory
import os
import markdown
from markupsafe import Markup

def create_app():
    app = Flask(__name__)
    
    # Set configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.analysis import analysis_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
    
    # Register markdown filter for templates
    @app.template_filter('markdown')
    def markdown_filter(text):
        if text is None:
            return ""
        return Markup(markdown.markdown(
            text, 
            extensions=['fenced_code', 'tables', 'nl2br']
        ))
    
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Serve uploaded files."""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    return app