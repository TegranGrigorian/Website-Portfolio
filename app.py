from flask import Flask, render_template, Blueprint, request, jsonify
from pages.main import main_bp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Explicitly load the .env file
load_dotenv(dotenv_path=".env")  # Load .env file from the current directory

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(contact_bp)
    @app.route("/resume/")
    def resume():
        return render_template("resume.html")

    @app.route("/test-fonts/")
    def test_fonts():
        return render_template("test-fonts.html")

    return app

#email backend code because making a separate file for it is too much work

contact_bp = Blueprint('contact', __name__)

@contact_bp.route("/send-email", methods=["POST"])
def send_email():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        print(f"Name: {name}, Email: {email}, Message: {message}")

        sender_email = os.getenv("sender_email")
        sender_password = os.getenv("app_password")
        recipient_email = os.getenv("receiver_email")

        if not sender_email or not sender_password or not recipient_email:
            raise ValueError("Missing email configuration in .env file")

        subject = f"Portfolio Contact Form: Message from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return jsonify({"success": True, "message": "Email sent successfully! Thank you for getting into contact ☺️☺️☺️"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)