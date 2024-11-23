from App.database import db
from datetime import datetime


class Ranking(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key=True)
    ranking_history_id = db.Column(db.Integer, db.ForeignKey('ranking_history.id'), nullable=False)
<<<<<<< HEAD
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=True) 
    rank = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __init__(self, ranking_history_id, competition_id, rank, colour, date):
        self.ranking_history_id = ranking_history_id
        self.competition_id = competition_id
        self.rank = rank
        self.colour = colour
        self.date = date
=======
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False) 
    rank = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __init__(self, ranking_history_id, student_id, competition_id, rank):
        self.ranking_history_id = ranking_history_id
        self.student_id = student_id
        self.competition_id = competition_id
        self.rank = rank
>>>>>>> b134881 (removed rank and ranking id from RankingHistory added it to Ranking)

    def get_json(self):
        return {
            "id" : self.id,
            "ranking_history_id" : self.ranking_history_id,
            "competition_id" : self.competition_id,
            "rank" : self.rank,
<<<<<<< HEAD
            "colour": self.colour,
            "date" : self.date 
=======
            "date" : self.date
>>>>>>> b134881 (removed rank and ranking id from RankingHistory added it to Ranking)
        }
    
    def to_Dict(self):
      return {
            "ID" : self.id,
            "Ranking History ID" : self.ranking_history_id,
            "Competition ID" : self.competition_id,
            "Rank" : self.rank,
<<<<<<< HEAD
            "Colour": self.colour,
=======
>>>>>>> b134881 (removed rank and ranking id from RankingHistory added it to Ranking)
            "Date": self.date
      }
