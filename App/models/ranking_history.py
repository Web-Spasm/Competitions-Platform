from App.database import db
from datetime import datetime


class RankingHistory(db.Model):
    __tablename__ = 'ranking_history'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, student_id,rank_id, rank):
        self.student_id = student_id
        self.rank_id = rank_id
        self.rank = rank

    def __repr__(self):
        return f'<RankingHistory {self.id} : {self.rank}>'
