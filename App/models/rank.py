from App.database import db
from datetime import datetime


class Rank(db.Model):
    __tablename__ = 'rank'

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False) 
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __init__(self, student_id, competition_id, rank):
        self.student_id = student_id
        self.competition_id = competition_id
        self.rank = rank

    def __repr__(self):
        return f'<Rank {self.id} : {self.rank}>'
