from App.database import db

# Association table to link students and student teams
student_team_association = db.Table('student_team_association',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('student_team_id', db.Integer, db.ForeignKey('student_team.id'), primary_key=True)
)

class StudentTeam(db.Model):
    __tablename__ = 'student_team'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50), nullable=False)
    students = db.relationship('Student', secondary=student_team_association, backref='teams', lazy=True, overlaps="members")

    def __init__(self, team_name):
        self.team_name = team_name

    def get_json(self):
        return {
            "id": self.id,
            "team_name": self.team_name,
            "students": [student.username for student in self.students]
        }

    def to_Dict(self):
        return {
            "ID": self.id,
            "Team Name": self.team_name,
            "Students": [student.username for student in self.students]
        }