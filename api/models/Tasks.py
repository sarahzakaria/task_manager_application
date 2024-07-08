from .base import db
from sqlalchemy.sql import func

class Tasks(db.Model):
    __tablename__ = "Tasks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    priority = db.Column(db.String(50), nullable=False)  # low, medium, high
    due_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Task {self.name} {self.id}>"