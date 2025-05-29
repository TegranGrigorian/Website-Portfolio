from flask import Blueprint, render_template #type: ignore python is idiot

about_bp = Blueprint('about', __name__, url_prefix="/about")

@about_bp.route("/")
def about():
    return render_template("about.html")
