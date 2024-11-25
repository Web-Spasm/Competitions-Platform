from App.database import db
from datetime import datetime


class Ranking(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key=True)
    ranking_history_id = db.Column(db.Integer, db.ForeignKey('ranking_history.id'), nullable=False)
<<<<<<< HEAD
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
=======
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=True) 
>>>>>>> 86b4459 (Edited student, ranking, ranking_history and modertor contollers, edited ranking model and initialsation commands)
    rank = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __init__(self, ranking_history_id, competition_id, rank, colour, date):
        self.ranking_history_id = ranking_history_id
        self.competition_id = competition_id
        self.rank = rank
<<<<<<< HEAD
>>>>>>> b134881 (removed rank and ranking id from RankingHistory added it to Ranking)
=======
        self.colour = colour
        self.date = date
>>>>>>> 86b4459 (Edited student, ranking, ranking_history and modertor contollers, edited ranking model and initialsation commands)

    def get_json(self):
        return {
            "id" : self.id,
            "ranking_history_id" : self.ranking_history_id,
            "competition_id" : self.competition_id,
            "rank" : self.rank,
<<<<<<< HEAD
<<<<<<< HEAD
            "colour": self.colour,
            "date" : self.date 
=======
            "date" : self.date
>>>>>>> b134881 (removed rank and ranking id from RankingHistory added it to Ranking)
=======
            "colour": self.colour,
            "date" : self.date 
>>>>>>> 86b4459 (Edited student, ranking, ranking_history and modertor contollers, edited ranking model and initialsation commands)
        }
    
    def to_Dict(self):
      return {
            "ID" : self.id,
            "Ranking History ID" : self.ranking_history_id,
            "Competition ID" : self.competition_id,
            "Rank" : self.rank,
<<<<<<< HEAD
<<<<<<< HEAD
            "Colour": self.colour,
=======
>>>>>>> b134881 (removed rank and ranking id from RankingHistory added it to Ranking)
=======
            "Colour": self.colour,
>>>>>>> 86b4459 (Edited student, ranking, ranking_history and modertor contollers, edited ranking model and initialsation commands)
            "Date": self.date
      }
