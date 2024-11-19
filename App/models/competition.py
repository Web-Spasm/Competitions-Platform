from App.database import db
from datetime import datetime
from .competition_moderator import *
from .competition_team import *

class Competition(db.Model):
    __tablename__='competition'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default= datetime.utcnow)
    location = db.Column(db.String(120), nullable=False)
    level = db.Column(db.Float, default=1)
    max_score = db.Column(db.Integer, default=25)
    confirm = db.Column(db.Boolean, default=False)
    moderators = db.relationship('Moderator', secondary="competition_moderator", overlaps='competitions', lazy=True)
    competition_teams = db.relationship('CompetitionTeam', backref='competition', lazy=True)

    def __init__(self, name, date, location, level, max_score):
        self.name = name
        self.date = date
        self.location = location
        self.level = level
        self.max_score = max_score
        self.moderators = []
        self.competition_teams = []
    
    def add_mod(self, mod):
        for m in self.moderators:
            if m.id == mod.id:
                print(f'{mod.username} already added to {self.name}!')
                return None
        
        comp_mod = CompetitionModerator(comp_id=self.id, mod_id=mod.id)
        try:
            self.moderators.append(mod)
            mod.competitions.append(self)
            db.session.commit()
            print(f'{mod.username} was added to {self.name}!')
            return comp_mod
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None

    def add_student_team(self, student_team):
        for ct in self.competition_teams:
            if ct.student_team_id == student_team.id:
                print(f'Team already registered for {self.name}!')
                return None
        
        comp_team = CompetitionTeam(comp_id=self.id, student_team_id=student_team.id)
        try:
            self.competition_teams.append(comp_team)
            db.session.commit()
            print(f'{student_team.team_name} was added to {self.name}!')
            return comp_team
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None

    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.strftime("%d-%m-%Y"),
            "location": self.location,
            "level" : self.level,
            "max_score" : self.max_score,
            "moderators": [mod.username for mod in self.moderators],
            "teams": [ct.student_team.team_name for ct in self.competition_teams]
        }

    def toDict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Date": self.date,
            "Location": self.location,
            "Level" : self.level,
            "Max Score" : self.max_score,
            "Moderators": [mod.username for mod in self.moderators],
            "Teams": [ct.student_team.team_name for ct in self.competition_teams]
        }

    def __repr__(self):
        return f'<Competition {self.id} : {self.name}>'