# app.py
import os
from flask import (
    Flask, render_template, redirect, url_for, flash,
    request, send_from_directory
)
from werkzeug.utils import secure_filename
from config import Config

# ---------------- App Setup ----------------
app = Flask(__name__)
app.config.from_object(Config)

# ---------------- Database ----------------
from models import db, Project, Contact
db.init_app(app)

# ---------------- Utils ----------------
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# ---------------- Routes ----------------

@app.route("/")
def home():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    contact = Contact.query.first()
    return render_template("home.html", projects=projects, contact=contact)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/education")
def education():
    return render_template("education_experience.html")

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/projects")
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("projects.html", projects=projects)

@app.route("/projects/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("project_detail.html", project=project)

@app.route("/resume")
def resume():
    return render_template("resume_download.html")

@app.route("/download_resume")
def download_resume():
    directory = os.path.join(app.root_path, "static", "files")
    filename = "resume.pdf"
    return send_from_directory(directory, filename, as_attachment=True)

# ---------------- Contact (DISPLAY ONLY) ----------------
@app.route("/contact")
def contact_me():
    contact = Contact.query.first()
    return render_template("contact.html", contact=contact)

# ---------------- Admin: Create Project ----------------
@app.route("/admin/projects/new", methods=["GET", "POST"])
def admin_create_project():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        short_description = request.form.get("short_description", "").strip()
        description = request.form.get("description", "").strip()
        tech_stack = request.form.get("tech_stack", "").strip()
        img = request.files.get("image")

        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("admin_create_project"))

        filename = None
        if img and img.filename:
            if allowed_file(img.filename):
                filename = secure_filename(img.filename)
                img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            else:
                flash("Invalid image type.", "error")
                return redirect(url_for("admin_create_project"))

        project = Project(
            title=title,
            short_description=short_description,
            description=description,
            tech_stack=tech_stack,
            image_filename=filename
        )
        db.session.add(project)
        db.session.commit()

        flash("Project created successfully.", "success")
        return redirect(url_for("projects"))

    return render_template("admin_project_form.html", action="Create", project=None)

# ---------------- Admin: Edit Project ----------------
@app.route("/admin/projects/<int:project_id>/edit", methods=["GET", "POST"])
def admin_edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        short_description = request.form.get("short_description", "").strip()
        description = request.form.get("description", "").strip()
        tech_stack = request.form.get("tech_stack", "").strip()
        img = request.files.get("image")

        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("admin_edit_project", project_id=project.id))

        if img and img.filename:
            if allowed_file(img.filename):
                filename = secure_filename(img.filename)
                img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                project.image_filename = filename
            else:
                flash("Invalid image type.", "error")
                return redirect(url_for("admin_edit_project", project_id=project.id))

        project.title = title
        project.short_description = short_description
        project.description = description
        project.tech_stack = tech_stack

        db.session.commit()
        flash("Project updated successfully.", "success")
        return redirect(url_for("project_detail", project_id=project.id))

    return render_template("admin_project_form.html", action="Edit", project=project)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ---------------- App Start ----------------
# ---------------- App Start ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # ensure one contact row exists
        if Contact.query.count() == 0:
            contact = Contact(
                email="",
                phone="",
                location="",
                linkedin="",
                github="",
                leetcode="",
                instagram=""
            )
            db.session.add(contact)
            db.session.commit()

    app.run()
