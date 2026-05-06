from flask import Flask, render_template, Blueprint, request, jsonify
from pages.main import main_bp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
import re

# Explicitly load the .env file
load_dotenv(dotenv_path=".env")  # Load .env file from the current directory

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(contact_bp)
    # @app.route("/resume/")
    # def resume():
    #     return render_template("resume.html")

    @app.route("/test-fonts/")
    def test_fonts():
        return render_template("test-fonts.html")

    return app

#email backend code because making a separate file for it is too much work

contact_bp = Blueprint('contact', __name__)

@contact_bp.route("/send-email", methods=["POST"])
def send_email():
    try:
        name    = request.form.get("name", "").strip()
        email   = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        files   = request.files.getlist("attachments")

        # Basic server-side validation
        if not name or not email or not message:
            return jsonify({"success": False, "message": "Missing required fields."}), 400
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({"success": False, "message": "Invalid email address."}), 400

        sender_email    = os.getenv("sender_email")
        sender_password = os.getenv("app_password")
        recipient_email = os.getenv("receiver_email")

        if not sender_email or not sender_password or not recipient_email:
            raise ValueError("Missing email configuration in .env file")

        subject = f"Portfolio Contact: Message from {name}"

        # Plain-text body
        plain_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # HTML body — convert [label](url) markdown links to <a> tags
        def text_to_html(text):
            escaped = (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))
            # Convert [label](url)
            linked = re.sub(
                r'\[([^\]]+)\]\((https?://[^)]+)\)',
                r'<a href="\2">\1</a>',
                escaped
            )
            return linked.replace("\n", "<br>\n")

        html_body = f"""<html><body style="font-family:sans-serif; color:#222; line-height:1.6;">
<p><strong>From:</strong> {name}<br>
<strong>Reply-to:</strong> {email}</p>
<hr style="border:none; border-top:1px solid #ddd;">
<p>{text_to_html(message)}</p>
</body></html>"""

        # Build email: outer container is multipart/mixed for attachments
        outer = MIMEMultipart("mixed")
        outer["From"]    = sender_email
        outer["To"]      = recipient_email
        outer["Subject"] = subject
        outer["Reply-To"] = email

        # Attach plain + HTML as alternatives
        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(plain_body, "plain", "utf-8"))
        alt.attach(MIMEText(html_body,  "html",  "utf-8"))
        outer.attach(alt)

        # Attach uploaded files
        allowed_extensions = {
            ".pdf", ".doc", ".docx", ".txt",
            ".png", ".jpg", ".jpeg", ".gif",
            ".zip", ".csv", ".mp4"
        }
        max_attach_bytes = 10 * 1024 * 1024  # 10 MB total
        total_size = 0
        for f in files:
            if not f or not f.filename:
                continue
            ext = os.path.splitext(f.filename)[1].lower()
            if ext not in allowed_extensions:
                continue
            data = f.read()
            total_size += len(data)
            if total_size > max_attach_bytes:
                break  # silently stop adding more files
            part = MIMEBase("application", "octet-stream")
            part.set_payload(data)
            encoders.encode_base64(part)
            safe_name = os.path.basename(f.filename)
            part.add_header("Content-Disposition", "attachment", filename=safe_name)
            outer.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, outer.as_string())

        return jsonify({"success": True, "message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)