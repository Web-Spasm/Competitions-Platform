from datetime import date
from App.database import db
from App.models import Student, Competition, Notification, CompetitionTeam
from App.controllers import ranking, ranking_history
from App.models.ranking_history import RankingHistory

def create_student(username, password):
    student = get_student_by_username(username)
    if student:
        print(f'{username} already exists!')
        return None

    newStudent = Student(username=username, password=password)
    try:
        db.session.add(newStudent)
        db.session.commit()

        print(f'New Student: {username} created!')  
        return newStudent
    
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()


def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json

def update_student(id, username):
    student = get_student(id)
    if student:
        student.username = username
        try:
            db.session.add(student)
            db.session.commit()
            print("Username was updated!")
            return student
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

def display_student_info(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        competitions = []
        
        for team in student.teams:
            team_comps = CompetitionTeam.query.filter_by(team_id=team.id).all()
            for comp_team in team_comps:
                comp = Competition.query.filter_by(id=comp_team.comp_id).first()
                competitions.append(comp.name)

        profile_info = {
            "profile" : student.get_json(),
            "competitions" : competitions
        }

        return profile_info

def display_notifications(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        return {"notifications":[notification.to_Dict() for notification in student.notifications]}

def update_rankings(competition):
    students = get_all_students()
    
    #for unranked students
    for student in students:
        student_history = ranking_history.get_ranking_history_by_id(student.id)

        if not student_history:
            student_history = RankingHistory(student_id=student.id, date=competition.date)
            db.session.add(student_history)
            db.session.commit()

        if student.curr_rank == 0:
            student_ranking = ranking.create_ranking(student_history.id, competition.id, 0 , 'gray' ,competition.date)

    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)

    leaderboard = []
    count = 1

    curr_high = students[0].rating_score
    curr_rank = 1

    for student in students:
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        student_history = ranking_history.get_ranking_history_by_id(student.id)

        if student.comp_count != 0:
            leaderboard.append({"placement": curr_rank, "student": student.username, "rating score":student.rating_score})
            count += 1

            student.curr_rank = curr_rank

            if student.prev_rank == 0:
                message = f'RANK : {student.curr_rank}. Congratulations on your first rank!'
                student_ranking = ranking.create_ranking(student_history.id, competition.id, curr_rank, 'green' ,competition.date)
            elif student.curr_rank == student.prev_rank:
                message = f'RANK : {student.curr_rank}. Well done! You retained your rank after competition {competition.name}'
                student_ranking = ranking.create_ranking(student_history.id, competition.id, curr_rank, 'blue' ,competition.date)
            elif student.curr_rank < student.prev_rank:
                message = f'RANK : {student.curr_rank}. Congratulations! Your rank has went up after competition {competition.name}'
                student_ranking = ranking.create_ranking(student_history.id, competition.id, curr_rank,'green' ,competition.date)
            else:
                message = f'RANK : {student.curr_rank}. Oh no! Your rank has went down due to competition {competition.name}'
                student_ranking = ranking.create_ranking(student_history.id, competition.id, curr_rank, 'red' ,competition.date)

            student.prev_rank = student.curr_rank
            notification = Notification(student.id, message, competition.date)
            student.notifications.append(notification)

            try:
                db.session.add(student)
                db.session.add(student_ranking)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

    return leaderboard

def display_rankings():
    students = get_all_students()

    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)

    leaderboard = []
    count = 1
    curr_high = students[0].rating_score
    curr_rank = 1
        
    for student in students:
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        if student.comp_count != 0:
            leaderboard.append({"placement": curr_rank, "student": student.username, "rating score":student.rating_score})
            count += 1

    print("Rank\tStudent\tRating Score")

    for position in leaderboard:
        print(f'{position["placement"]}\t{position["student"]}\t{position["rating score"]}')
    
    return leaderboard