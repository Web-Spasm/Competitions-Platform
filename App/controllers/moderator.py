from App.database import db
from App.models import Moderator, Competition, Team, CompetitionTeam, RankingHistory, Ranking

def create_moderator(username, password):
    mod = get_moderator_by_username(username)
    if mod:
        print(f'{username} already exists!')
        return None

    newMod = Moderator(username=username, password=password)
    try:
        db.session.add(newMod)
        db.session.commit()
        print(f'New Moderator: {username} created!')
        return newMod
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_moderator_by_username(username):
    return Moderator.query.filter_by(username=username).first()

def get_moderator(id):
    return Moderator.query.get(id)

def get_all_moderators():
    return Moderator.query.all()

def get_all_moderators_json():
    mods = Moderator.query.all()
    if not mods:
        return []
    mods_json = [mod.get_json() for mod in mods]
    return mods_json

def update_moderator(id, username):
    mod = get_moderator(id)
    if mod:
        mod.username = username
        try:
            db.session.add(mod)
            db.session.commit()
            print("Username was updated!")
            return mod
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

def add_mod(mod1_name, comp_name, mod2_name):
    mod1 = Moderator.query.filter_by(username=mod1_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()
    mod2 = Moderator.query.filter_by(username=mod2_name).first()

    if not mod1:
        print(f'Moderator: {mod1_name} not found!')
        return None
    elif not comp:
        print(f'Competition: {comp_name} not found!')
        return None
    elif not mod2:
        print(f'Moderator: {mod2_name} not found!')
        return None
    elif not mod1 in comp.moderators:
        print(f'{mod1_name} is not authorized to add results for {comp_name}!')
        return None
    else:
        return comp.add_mod(mod2)
    
def calculate_competition_team_scores(score, max_score, level, factor=100):
    normalized_score = score / max_score
    weighted_score = normalized_score * level * factor  
    return score, weighted_score

def update_student_rating(current_rating, comp_count, new_weighted_score):
    return (current_rating * comp_count + new_weighted_score)/(comp_count + 1)
                
def add_results(mod_name, comp_name, team_name, score):
    mod = Moderator.query.filter_by(username=mod_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()
    teams = Team.query.filter_by(name=team_name).all()

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
            for team in teams:
                comp_team = CompetitionTeam.query.filter_by(comp_id=comp.id, team_id=team.id).first()

                if comp_team:
                    points_earned, rating_score = calculate_competition_team_scores(score, comp.max_score, comp.level)
                    individual_score = rating_score / len(team.students)  # Normalize by team size
                    comp_team.points_earned = points_earned
                    comp_team.rating_score = rating_score
                    try:
                        db.session.add(comp_team)
                        db.session.commit()
                        print(f'Score successfully added for {team_name}!')

                        # adjusted to create or update ranking history
                        for student in team.students:
                            ranking_history = RankingHistory.query.filter_by(student_id=student.id).first()
                            if not ranking_history:
                                ranking_history = RankingHistory(student_id=student.id, date=comp.date)
                                db.session.add(ranking_history)
                                db.session.commit()
                            
                            ranking = Ranking(ranking_history_id=ranking_history.id, competition_id=comp.id, rank=comp_team.points_earned, colour="", date="")
                            db.session.add(ranking)
                            db.session.commit()

                            student.rating_score = update_student_rating(student.rating_score, student.comp_count, individual_score)
                            student.comp_count += 1
                            db.session.add(student)
                            db.session.commit()

                        return comp_team
                    except Exception as e:
                        db.session.rollback()
                        print(f"Something went wrong: {e}")
                        return None
    return None


def update_ratings(mod_name, comp_name):
    mod = Moderator.query.filter_by(username=mod_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()

    if not mod:
        print(f'{mod_name} was not found!')
        return None
    elif not comp:
        print(f'{comp_name} was not found!')
        return None
    elif comp.confirm:
        print(f'Results for {comp_name} has already been finalized!')
        return None
    elif mod not in comp.moderators:
        print(f'{mod_name} is not authorized to add results for {comp_name}!')
        return None
    elif len(comp.teams) == 0:
        print(f'No teams found. Results can not be confirmed!')
        return None
    else:
        comp_teams = CompetitionTeam.query.filter_by(comp_id=comp.id).all()

        for comp_team in comp_teams:
            team = Team.query.filter_by(id=comp_team.team_id).first()

            for stud in team.students:
                weighted_score = comp_team.rating_score / len(team.students)  # Normalize by team size
                stud.rating_score = update_student_rating(stud.rating_score, stud.comp_count, weighted_score)
                stud.comp_count += 1
                try:
                    db.session.add(stud)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Something went wrong: {e}")

        comp.confirm = True
        db.session.add(comp)
        db.session.commit()
        print("Results finalized!")
        return True