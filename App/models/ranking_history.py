from App.database import db
from datetime import datetime


class RankingHistory(db.Model):
    __tablename__ = 'ranking_history'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, student_id, date):
        self.student_id = student_id
        self.date = date
      

    def get_json(self):
        return {
            "id" : self.id,
            "student_id" : self.student_id,
            "date" : self.date
        }
    
    def to_Dict(self):
      return {
            "ID" : self.id,
            "Student ID" : self.student_id,
            "Date" : self.date
      }
