from app import app
from models import db, Contact

with app.app_context():
    contact = Contact.query.first()
    if not contact:
        contact = Contact()
        db.session.add(contact)

    contact.email = "harshitalohia@gmail.com"
    contact.phone = "+918610613039"
    contact.linkedin = "https://www.linkedin.com/in/harshita-lohia-b9a5b7337/"
    contact.github = "https://github.com/harshitalohia19"
    contact.leetcode = "https://leetcode.com/u/harshitalohia/"
    contact.instagram = "https://www.instagram.com/_.harshita19._?igsh=YWN4bXdzejlrZDJy"

    db.session.commit()
    print("Contact info updated successfully")
