from flask import Flask, render_template
from pages.main import main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)

    @app.route("/resume/")
    def resume():
        return render_template("resume.html")

    @app.route("/test-fonts/")
    def test_fonts():
        return render_template("test-fonts.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
