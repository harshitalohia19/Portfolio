# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    short_description = db.Column(db.String(300))
    description = db.Column(db.Text)
    tech_stack = db.Column(db.String(300))  # comma separated
    image_filename = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def image_url(self):
        if self.image_filename:
            return f"/uploads/{self.image_filename}"
        return "/static/images/placeholder.png"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    location = db.Column(db.String(200))

    linkedin = db.Column(db.String(300))
    github = db.Column(db.String(300))
    leetcode = db.Column(db.String(300))
    instagram = db.Column(db.String(300))

