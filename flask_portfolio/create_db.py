from app import db, app
from models import Project, Contact

with app.app_context():
    db.create_all()
    # create default contact row if none
    if Contact.query.count() == 0:
        c = Contact(email="", phone="", location="", linkedin="", github="", about="")
        db.session.add(c)
        db.session.commit()
    print("Database created and default contact row ensured.")
