from flask import Blueprint, render_template # type: ignore python is idiot

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")
