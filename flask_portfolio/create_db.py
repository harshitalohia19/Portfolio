# create_db.py
from app import app
from flask_portfolio.models import db, Project
with app.app_context():
    db.create_all()
    if Contact.query.count() == 0:
        c = Contact(email="", phone="", location="", linkedin="", github="", about="")
        db.session.add(c)
        db.session.commit()
    print("Database created and default contact row ensured.")
