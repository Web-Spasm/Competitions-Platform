from App.database import db
from datetime import datetime


class Ranking(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key=True)
    ranking_history_id = db.Column(db.Integer, db.ForeignKey('ranking_history.id'), nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=True) 
    rank = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __init__(self, ranking_history_id, competition_id, rank, colour, date=None):
        self.ranking_history_id = ranking_history_id
        self.competition_id = competition_id
        self.rank = rank
        self.colour = colour
        self.date = date

    def get_json(self):
        return {
            "id" : self.id,
            "ranking_history_id" : self.ranking_history_id,
            "competition_id" : self.competition_id,
            "rank" : self.rank,
            "colour": self.colour,
            "date" : self.date 
        }
    
    def to_Dict(self):
      return {
            "ID" : self.id,
            "Ranking History ID" : self.ranking_history_id,
            "Competition ID" : self.competition_id,
            "Rank" : self.rank,
            "Colour": self.colour,
            "Date": self.date
      }
