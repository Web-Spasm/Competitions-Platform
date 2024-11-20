from App.database import db
from App.models import User


class State(db.Model):
    __tablename__ = 'state'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)

    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

    def __repr__(self):
        return f"State(name={self.name}, abbreviation={self.abbreviation})"

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"
