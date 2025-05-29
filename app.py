from flask import Flask
from pages.main import main_bp
from pages.about import about_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(about_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
