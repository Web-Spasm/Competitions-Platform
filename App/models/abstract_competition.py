from App.database import db


class AbstractCompetition(db.Model):
    __tablename__="abstract_competition"

    id = db.Column(db.Integer, primary_key = True)

    def add_team():
        pass

    def remove_team():
        pass

    def notify(self):
        pass