from App.database import db
from App.models import Ranking, RankingHistory, Competition
from datetime import datetime

def create_ranking(ranking_history_id, competition_id, rank, colour, date):
    ranking_history = RankingHistory.query.get(ranking_history_id)
    if not ranking_history:
        print(f'Ranking History with ID: {ranking_history_id} not found!')
        return None
    competition = Competition.query.get(competition_id)
    if not competition:
        print(f'Competition with ID: {competition_id} not found!')
        return None
    new_ranking = Ranking(ranking_history_id=ranking_history_id, competition_id=competition_id, rank=rank, colour=colour, date=date)
    try:
        db.session.add(new_ranking)
        db.session.commit()
        print(f'New Ranking for competition with ID: {competition_id} created!')
        return new_ranking
    except Exception as e:
        db.session.rollback()
        print("Ranking creation failed!")
        return None

def get_ranking_by_id(ranking_id):
    ranking = Ranking.query.get(ranking_id).first()
    if not ranking:
        print(f'Ranking with ID: {ranking_id} not found!')
        return None
    return ranking

def get_rankings_by_history_id(ranking_history_id):
    rankings = Ranking.query.filter_by(ranking_history_id=ranking_history_id).all()
    if rankings:
        return rankings

    print(f'Rankings for {ranking_history_id} not found.')
    return None 

def get_rankings_by_id_json(ranking_id):
    ranking = Ranking.query.get(ranking_id).first()
    if not ranking:
        print(f'Ranking with ID: {ranking_id} not found!')
        return None
    return ranking.get_json()

def update_ranking(ranking_id, ranking_history_id, competition_id, rank, colour,  date):
    ranking = Ranking.query.get(ranking_id)
    if not ranking:
        print(f'Ranking with ID: {ranking_id} not found!')
        return None
    ranking.ranking_history_id = ranking_history_id
    ranking.competition_id = competition_id
    ranking.rank = rank
    ranking.colour = colour
    ranking.date = datetime.strptime(date, "%d-%m-%Y")
    try:
        db.session.commit()
        print(f'Ranking with ID: {ranking_id} updated!')
        return ranking
    except Exception as e:
        db.session.rollback()
        print("Ranking update failed!")
        return None