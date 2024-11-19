from App.database import db

class CompetitionTeam(db.Model):
    __tablename__ = 'competition_team'

    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    student_team_id = db.Column(db.Integer, db.ForeignKey('student_team.id'), nullable=False)
    points_earned = db.Column(db.Float, default=0)
    rating_score = db.Column(db.Float, default=0)
    ranking = db.Column(db.Integer, default=0)

    student_team = db.relationship('StudentTeam', backref='competition_teams')

    def __init__(self, comp_id, student_team_id):
        self.comp_id = comp_id
        self.student_team_id = student_team_id
        self.points_earned = 0
        self.rating_score = 0
        self.ranking = 0

    def update_points(self, points_earned):
        self.points_earned = points_earned

    def update_rating(self, rating_score):
        self.rating_score = rating_score

    def update_ranking(self, ranking):
        self.ranking = ranking

    def get_json(self):
        return {
            "id": self.id,
            "student_team_id": self.student_team_id,
            "competition_id": self.comp_id,
            "points_earned": self.points_earned,
            "rating_score": self.rating_score,
            "ranking": self.ranking
        }

    def toDict(self):
        return {
            "ID": self.id,
            "Student Team ID": self.student_team_id,
            "Competition ID": self.comp_id,
            "Points Earned": self.points_earned,
            "Rating Score": self.rating_score,
            "Ranking": self.ranking
        }