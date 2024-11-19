from App.database import db
from App.models import StudentTeam, Competition, Student, Moderator, CompetitionTeam

def create_student_team(team_name, students):
    student_team = StudentTeam(team_name=team_name)
    count = 0
    for s in students:
        stud = Student.query.filter_by(username=s).first()
        if stud:
            student_team.students.append(stud)
        else:
            count += 1
            print(f'{s} was not found!')
    
    if count == len(students):
        return None
    else:
        try:
            db.session.add(student_team)
            db.session.commit()
            print(f'New Student Team: {team_name} created!')
            return student_team
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None

def get_student_team_by_name(name):
    return StudentTeam.query.filter_by(team_name=name).first()

def get_student_team(id):
    return StudentTeam.query.get(id)

def get_all_student_teams():
    return StudentTeam.query.all()

def get_all_student_teams_json():
    student_teams = StudentTeam.query.all()

    if not student_teams:
        return []
    else:
        return [team.get_json() for team in student_teams]
    
def find_student_team(team_name, students):
    student_teams = StudentTeam.query.filter_by(team_name=team_name).all()
    
    for team in student_teams:
        team_stud = []
        for stud in team.students:
            team_stud.append(stud.username)
        
        if set(team_stud) == set(students):
            return team

    return None

def add_student_team(mod_name, comp_name, team_name, students):
    mod = Moderator.query.filter_by(username=mod_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()
    
    if not mod:
        print(f'Moderator: {mod_name} not found!')
        return None
    elif not comp:
        print(f'Competition: {comp_name} not found!')
        return None
    elif comp.confirm:
        print(f'Results for {comp_name} have already been finalized!')
        return None
    elif mod not in comp.moderators:
        print(f'{mod_name} is not authorized to add teams for {comp_name}!')
        return None
    else:
        student_team = find_student_team(team_name, students)

        if student_team:
            return comp.add_student_team(student_team)
        
        comp_students = []
        
        for team in comp.competition_teams:
            for stud in team.student_team.students:
                comp_students.append(stud.username)
        
        for stud in students:
            if stud in comp_students:
                print(f'{stud} is already registered for {comp_name}!')
                print(f'Team was not created!')
                return None
        
        student_team = create_student_team(team_name, students)
        
        if student_team:
            return comp.add_student_team(student_team)
        else:
            return None

def add_results(mod_name, comp_name, team_name, students, score):
    add_student_team(mod_name, comp_name, team_name, students)
    
    mod = Moderator.query.filter_by(username=mod_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()
    student_teams = StudentTeam.query.filter_by(team_name=team_name).all()

    if not mod:
        print(f'{mod_name} was not found!')
        return None
    else:
        if not comp:
            print(f'{comp_name} was not found!')
            return None
        elif comp.confirm:
            print(f'Results for {comp_name} have already been finalized!')
            return None
        elif mod not in comp.moderators:
            print(f'{mod_name} is not authorized to add results for {comp_name}!')
            return None
        else:
            for student_team in student_teams:
                comp_team = CompetitionTeam.query.filter_by(comp_id=comp.id, student_team_id=student_team.id).first()

                if comp_team:
                    comp_team.points_earned = score
                    comp_team.rating_score = (score / comp.max_score) * 20 * comp.level
                    try:
                        db.session.add(comp_team)
                        db.session.commit()
                        print(f'Score successfully added for {team_name}!')
                        return comp_team
                    except Exception as e:
                        db.session.rollback()
                        print("Something went wrong!")
                        return None
    return None