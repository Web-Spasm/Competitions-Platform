from App.database import db
from App.models import Student, RankingHistory
from datetime import datetime

def create_ranking_history(student_id, date):
    student = Student.query.get(student_id)
    if not student:
        print(f'Student with ID: {student_id} not found!')
        return None
    new_ranking_history = RankingHistory(student_id=student_id, date=datetime.strptime(date, "%d-%m-%Y"))
    try:
        db.session.add(new_ranking_history)
        db.session.commit()
        print(f'New Ranking History for student with ID: {student_id} created!')
        return new_ranking_history
    except Exception as e:
        db.session.rollback()
        print("Ranking History creation failed!")
        return None

def get_ranking_history_by_id(student_id):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    ranking_history = RankingHistory.query.filter_by(student_id=student_id).first()
=======
    ranking_history = RankingHistory.query.get(student_id)
>>>>>>> 26f665b (Added Null checks in ranking history and ranking)
=======
    ranking_history = RankingHistory.query.filter_by(student_id=student_id).first()
>>>>>>> 86b4459 (Edited student, ranking, ranking_history and modertor contollers, edited ranking model and initialsation commands)
    if not ranking_history:
        print(f'Ranking History for student with ID: {student_id} not found!')
        return None
    return ranking_history
<<<<<<< HEAD

def get_ranking_history_by_id_json(student_id):
    ranking_history = RankingHistory.query.get(student_id).first()
    if not ranking_history:
        print(f'Ranking History for student with ID: {student_id} not found!')
=======
    return RankingHistory.query.get(student_id)
=======
>>>>>>> 26f665b (Added Null checks in ranking history and ranking)

def get_ranking_history_by_id_json(student_id):
    ranking_history = RankingHistory.query.get(student_id).first()
    if not ranking_history:
<<<<<<< HEAD
>>>>>>> 27d47c7 (Added controllers for Ranking History and Ranking, also modified the Moderators's add_results function)
=======
        print(f'Ranking History for student with ID: {student_id} not found!')
>>>>>>> 26f665b (Added Null checks in ranking history and ranking)
        return None
    return ranking_history.get_json()

def update_ranking_history(student_id, date):
    ranking_history = RankingHistory.query.get(student_id)
    if not ranking_history:
        print(f'Ranking History for student with ID: {student_id} not found!')
        return None
    ranking_history.date = datetime.strptime(date, "%d-%m-%Y")
    try:
        db.session.commit()
        print(f'Ranking History for student with ID: {student_id} updated!')
        return ranking_history
    except Exception as e:
        db.session.rollback()
        print("Ranking History update failed!")
<<<<<<< HEAD
<<<<<<< HEAD
        return None
=======
        return None
>>>>>>> 27d47c7 (Added controllers for Ranking History and Ranking, also modified the Moderators's add_results function)
=======
        return None
>>>>>>> 26f665b (Added Null checks in ranking history and ranking)
