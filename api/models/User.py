from .base import db
from sqlalchemy.sql import func

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    tasks = db.relationship("Tasks", backref="user")
    is_admin = db.Column(db.Boolean, default=False, nullable=False)  # Add the is_admin field

    def __repr__(self):
        return f"<User {self.firstName} {self.id}>"