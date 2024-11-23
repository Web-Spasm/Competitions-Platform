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
    ranking_history = RankingHistory.query.filter_by(student_id=student_id).first()
    if not ranking_history:
        print(f'Ranking History for student with ID: {student_id} not found!')
        return None
    return ranking_history

def get_ranking_history_by_id_json(student_id):
    ranking_history = RankingHistory.query.get(student_id).first()
    if not ranking_history:
        print(f'Ranking History for student with ID: {student_id} not found!')
=======
    return RankingHistory.query.get(student_id)

def get_ranking_history_by_id_json(student_id):
    ranking_history = RankingHistory.query.get(student_id)
    if not ranking_history:
>>>>>>> 27d47c7 (Added controllers for Ranking History and Ranking, also modified the Moderators's add_results function)
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
        return None
=======
        return None
>>>>>>> 27d47c7 (Added controllers for Ranking History and Ranking, also modified the Moderators's add_results function)
