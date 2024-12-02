import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UnitTests(unittest.TestCase):
    #User Unit Tests
    def test_new_user(self):
        user = User("ryan", "ryanpass")
        assert user.username == "ryan"

    def test_hashed_password(self):
        password = "ryanpass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("ryan", password)
        assert user.password != password

    def test_check_password(self):
        password = "ryanpass"
        user = User("ryan", password)
        assert user.check_password(password)

    #Student Unit Tests
    def test_new_student(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      assert student.username == "james"

    def test_student_get_json(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      self.assertDictEqual(student.get_json(), {"id": None, "username": "james", "rating_score": 0, "comp_count": 0, "curr_rank": 0})

    #Moderator Unit Tests
    def test_new_moderator(self):
      db.drop_all()
      db.create_all()
      mod = Moderator("robert", "robertpass")
      assert mod.username == "robert"

    def test_moderator_get_json(self):
      db.drop_all()
      db.create_all()
      mod = Moderator("robert", "robertpass")
      self.assertDictEqual(mod.get_json(), {"id":None, "username": "robert", "competitions": []})
    
    #Team Unit Tests
    def test_new_team(self):
      db.drop_all()
      db.create_all()
      team = Team("Scrum Lords")
      assert team.name == "Scrum Lords"
    
    def test_team_get_json(self):
      db.drop_all()
      db.create_all()
      team = Team("Scrum Lords")
      self.assertDictEqual(team.get_json(), {"id":None, "name":"Scrum Lords", "students": []})
    
    #Competition Unit Tests
    def test_new_competition(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      assert competition.name == "RunTime" and competition.date.strftime("%d-%m-%Y") == "09-02-2024" and competition.location == "St. Augustine" and competition.level == 1 and competition.max_score == 25

    def test_competition_get_json(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      self.assertDictEqual(competition.get_json(), {"id": None, "name": "RunTime", "date": "09-02-2024", "location": "St. Augustine", "level": 1, "max_score": 25, "moderators": [], "teams": []})
    
    #Notification Unit Tests
    # def test_new_notification(self):
    #   db.drop_all()
    #   db.create_all()
    #   notification = Notification(1, "Ranking changed!")
    #   assert notification.student_id == 1 and notification.message == "Ranking changed!"

    # def test_notification_get_json(self):
    #   db.drop_all()
    #   db.create_all()
    #   notification = Notification(1, "Ranking changed!")
    #   self.assertDictEqual(notification.get_json(), {"id": None, "student_id": 1, "notification": "Ranking changed!"})

# update to include date
    """
    #Ranking Unit Tests
    def test_new_ranking(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      assert ranking.student_id == 1
  
    def test_set_points(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_points(15)
      assert ranking.total_points == 15

    def test_set_ranking(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_ranking(1)
      assert ranking.curr_ranking == 1

    def test_previous_ranking(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_previous_ranking(1)
      assert ranking.prev_ranking == 1

    def test_ranking_get_json(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_points(15)
      ranking.set_ranking(1)
      self.assertDictEqual(ranking.get_json(), {"rank":1, "total points": 15})
    """
    #CompetitionTeam Unit Tests
    def test_new_competition_team(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      assert competition_team.comp_id == 1 and competition_team.team_id == 1

    def test_competition_team_update_points(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      assert competition_team.points_earned == 15

    def test_competition_team_update_rating(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_rating(12)
      assert competition_team.rating_score == 12

    def test_competition_team_get_json(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      competition_team.update_rating(12)
      self.assertDictEqual(competition_team.get_json(), {"id": None, "team_id": 1, "competition_id": 1, "points_earned": 15, "rating_score": 12})

    #CompetitionModerator Unit Tests
    def test_new_competition_moderator(self):
      db.drop_all()
      db.create_all()
      competition_moderator = CompetitionModerator(1, 1)
      assert competition_moderator.comp_id == 1 and competition_moderator.mod_id == 1

    def test_competition_moderator_get_json(self):
      db.drop_all()
      db.create_all()
      competition_moderator = CompetitionModerator(1, 1)
      self.assertDictEqual(competition_moderator.get_json(), {"id": None, "competition_id": 1, "moderator_id": 1})

    #StudentTeam Unit Tests
    def test_new_student_team(self):
      db.drop_all()
      db.create_all()
      student_team = StudentTeam(1, 1)
      assert student_team.student_id == 1 and student_team.team_id == 1
    
    def test_student_team_get_json(self):
      db.drop_all()
      db.create_all()
      student_team = StudentTeam(1, 1)
      self.assertDictEqual(student_team.get_json(), {"id": None, "student_id": 1, "team_id": 1})

'''
    Integration Tests
'''
# This fixture creates an empty database for the test and deletes it after the test
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class RankingIntegrationTests(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_ranking_success(self):
        ranking_history = RankingHistory(student_id=1, date=datetime.now())
        ranking_history.id = 1
        competition = Competition(name="Test Competition", date=datetime.now(), location="Test Location", level=1, max_score=100)
        competition.id = 1
        db.session.add(ranking_history)
        db.session.add(competition)
        db.session.commit()

        result = create_ranking(1, 1, 1, 'red', datetime.now())
        self.assertIsNotNone(result)
        self.assertEqual(result.rank, 1)
        self.assertEqual(result.colour, 'red')

    def test_create_ranking_no_ranking_history(self):
        competition = Competition(name="Test Competition", date=datetime.now(), location="Test Location", level=1, max_score=100)
        competition.id = 1
        db.session.add(competition)
        db.session.commit()

        result = create_ranking(1, 1, 1, 'red', datetime.now())
        self.assertIsNone(result)

    def test_create_ranking_no_competition(self):
        ranking_history = RankingHistory(student_id=1, date=datetime.now())
        ranking_history.id = 1
        db.session.add(ranking_history)
        db.session.commit()

        result = create_ranking(1, 1, 1, 'red', datetime.now())
        self.assertIsNone(result)
    
    def test_get_ranking_by_id(self):
        ranking_history = RankingHistory(student_id=1, date=datetime.now())
        ranking_history.id = 1
        competition = Competition(name="Test Competition", date=datetime.now(), location="Test Location", level=1, max_score=100)
        competition.id = 1
        ranking = Ranking(ranking_history_id=1, competition_id=1, rank=1, colour='red', date=datetime.now())
        ranking.id = 1
        db.session.add(ranking_history)
        db.session.add(competition)
        db.session.add(ranking)
        db.session.commit()

        result = get_ranking_by_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, 1)
    
    def test_get_rankings_by_history_id(self):
        ranking_history = RankingHistory(student_id=1, date=datetime.now())
        ranking_history.id = 1
        competition = Competition(name="Test Competition", date=datetime.now(), location="Test Location", level=1, max_score=100)
        competition.id = 1
        ranking = Ranking(ranking_history_id=1, competition_id=1, rank=1, colour='red', date=datetime.now())
        db.session.add(ranking_history)
        db.session.add(competition)
        db.session.add(ranking)
        db.session.commit()

        result = get_rankings_by_history_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    def test_get_rankings_by_id_json(self):
        ranking_history = RankingHistory(student_id=1, date=datetime.now())
        ranking_history.id = 1
        competition = Competition(name="Test Competition", date=datetime.now(), location="Test Location", level=1, max_score=100)
        competition.id = 1
        ranking = Ranking(ranking_history_id=1, competition_id=1, rank=1, colour='red', date=datetime.now())
        ranking.id = 1
        db.session.add(ranking_history)
        db.session.add(competition)
        db.session.add(ranking)
        db.session.commit()

        result = get_rankings_by_id_json(1)
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 1)

    def test_update_ranking(self):
        ranking_history = RankingHistory(student_id=1, date=datetime.now())
        ranking_history.id = 1
        competition = Competition(name="Test Competition", date=datetime.now(), location="Test Location", level=1, max_score=100)
        competition.id = 1
        ranking = Ranking(ranking_history_id=1, competition_id=1, rank=1, colour='red', date=datetime.now())
        ranking.id = 1
        db.session.add(ranking_history)
        db.session.add(competition)
        db.session.add(ranking)
        db.session.commit()

        result = update_ranking(1, 1, 1, 2, 'blue', datetime.now().strftime("%d-%m-%Y"))
        self.assertIsNotNone(result)
        self.assertEqual(result.rank, 2)
        self.assertEqual(result.colour, 'blue')

class RankingHistoryIntegrationTests(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_ranking_history_success(self):
        student = Student(username="Test Student", password="password")
        student.id = 1
        db.session.add(student)
        db.session.commit()

        result = create_ranking_history(1, datetime.now())
        self.assertIsNotNone(result)
        self.assertEqual(result.student_id, 1)

    def test_create_ranking_history_no_student(self):
        result = create_ranking_history(1, datetime.now())
        self.assertIsNone(result)

    def test_get_ranking_history_by_id(self):
        student = Student(username="Test Student", password="password")
        student.id = 1
        ranking_history = RankingHistory(student_id=1, date=datetime.now())
        ranking_history.id = 1
        db.session.add(student)
        db.session.add(ranking_history)
        db.session.commit()

        result = get_ranking_history_by_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, 1)

    def test_get_ranking_history_by_id_json(self):
        student = Student(username="Test Student", password="password")
        student.id = 1
        ranking_history = RankingHistory(student_id=1, date=datetime.now())
        ranking_history.id = 1
        db.session.add(student)
        db.session.add(ranking_history)
        db.session.commit()

        result = get_ranking_history_by_id_json(1)
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 1)

    def test_update_ranking_history(self):
        student = Student(username="Test Student", password="password")
        student.id = 1
        ranking_history = RankingHistory(student_id=1, date=datetime.now())
        ranking_history.id = 1
        db.session.add(student)
        db.session.add(ranking_history)
        db.session.commit()

        result = update_ranking_history(1, datetime.now().strftime("%d-%m-%Y"))
        self.assertIsNotNone(result)
        self.assertEqual(result.date.strftime("%d-%m-%Y"), datetime.now().strftime("%d-%m-%Y"))

class ModeratorIntegrationTests(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_moderator_success(self):
        result = create_moderator("test_mod", "password")
        self.assertIsNotNone(result)
        self.assertEqual(result.username, "test_mod")
   
    def test_create_moderator_existing_username(self):
        create_moderator("test_mod", "password")
        result = create_moderator("test_mod", "password")
        self.assertIsNone(result)

    def test_get_moderator_by_username(self):
        create_moderator("test_mod", "password")
        result = get_moderator_by_username("test_mod")
        self.assertIsNotNone(result)
        self.assertEqual(result.username, "test_mod")

    def test_get_moderator(self):
        mod = create_moderator("test_mod", "password")
        result = get_moderator(mod.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.username, "test_mod")

    def test_get_all_moderators(self):
        create_moderator("test_mod1", "password")
        create_moderator("test_mod2", "password")
        result = get_all_moderators()
        self.assertEqual(len(result), 2)

    def test_get_all_moderators_json(self):
        create_moderator("test_mod1", "password")
        create_moderator("test_mod2", "password")
        result = get_all_moderators_json()
        self.assertEqual(len(result), 2)


    def test_update_moderator(self):
        mod = create_moderator("test_mod", "password")
        result = update_moderator(mod.id, "new_username")
        self.assertIsNotNone(result)
        self.assertEqual(result.username, "new_username")


    def test1_add_mod(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")
      comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      assert add_mod(mod1.username, comp.name, mod2.username) != None
       
    def test2_add_mod(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")
      mod3 = create_moderator("raymond", "raymondpass")
      comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      assert add_mod(mod2.username, comp.name, mod3.username) == None

     # Feature 2 Integration Tests
    def test1_add_results(self):
        mod = create_moderator("debra", "debrapass")
        comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
        student1 = create_student("james", "jamespass")
        student2 = create_student("steven", "stevenpass")
        student3 = create_student("emily", "emilypass")
        students = [student1.username, student2.username, student3.username]
        team = add_team(mod.username, comp.name, "Runtime Terrors", students)
        comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
        assert comp_team.points_earned == 15


    def test2_add_results(self):
        mod = create_moderator("debra", "debrapass")
        comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
        student1 = create_student("james", "jamespass")
        student2 = create_student("steven", "stevenpass")
        student3 = create_student("emily", "emilypass")
        student4 = create_student("mark", "markpass")
        student5 = create_student("eric", "ericpass")
        students = [student1.username, student2.username, student3.username]
        add_team(mod.username, comp.name, "Runtime Terrors", students)
        comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
        students = [student1.username, student4.username, student5.username]
        team = add_team(mod.username, comp.name, "Scrum Lords", students)
        assert team == None

    def test3_add_results(self):
        mod1 = create_moderator("debra", "debrapass")
        mod2 = create_moderator("robert", "robertpass")
        comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
        student1 = create_student("james", "jamespass")
        student2 = create_student("steven", "stevenpass")
        student3 = create_student("emily", "emilypass")
        students = [student1.username, student2.username, student3.username]
        team = add_team(mod2.username, comp.name, "Runtime Terrors", students)
        assert team == None

    def test_update_ratings(self):
        mod = create_moderator("mod", "password")
        comp = Competition(name="Test Competition", date=datetime.now(), location="Test Location", level=1, max_score=100)
        team = Team(name="Test Team")
        student = Student(username="student", password="password")
        student.name = "Test Student"
        student.rating_score = 0
        student.comp_count = 0
        team.students.append(student)
        db.session.add(comp)
        db.session.add(team)
        db.session.commit()
        comp.moderators.append(mod)
        db.session.commit()

        add_results("mod", "Test Competition", "Test Team", 90)
        result = update_ratings("mod", "Test Competition")
        self.assertTrue(result)
        self.assertTrue(comp.confirm)


class TestRatingCalculations(unittest.TestCase):

    def test_calculate_competition_team_scores(self):
        score, weighted_score = calculate_competition_team_scores(80, 100, 1.5)
        self.assertEqual(score, 80)
        self.assertAlmostEqual(weighted_score, 12.0, places=5)

        score, weighted_score = calculate_competition_team_scores(50, 100, 2)
        self.assertEqual(score, 50)
        self.assertAlmostEqual(weighted_score, 10.0, places=5)

        score, weighted_score = calculate_competition_team_scores(90, 90, 1)
        self.assertEqual(score, 90)
        self.assertAlmostEqual(weighted_score, 10.0, places=5)

    def test_update_student_rating(self):
        new_rating = update_student_rating(80, 10)
        self.assertAlmostEqual(new_rating, 90.0, places=5)

        new_rating = update_student_rating(70, 15)
        self.assertAlmostEqual(new_rating, 85.0, places=5)

        new_rating = update_student_rating(90, 5)
        self.assertAlmostEqual(new_rating, 95.0, places=5)




# class IntegrationTests(unittest.TestCase):
    
#     #Feature 1 Integration Tests
#     def test1_create_competition(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       assert comp.name == "RunTime" and comp.date.strftime("%d-%m-%Y") == "29-03-2024" and comp.location == "St. Augustine" and comp.level == 2 and comp.max_score == 25

#     def test2_create_competition(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       self.assertDictEqual(comp.get_json(), {"id": 1, "name": "RunTime", "date": "29-03-2024", "location": "St. Augustine", "level": 2, "max_score": 25, "moderators": ["debra"], "teams": []})
      
#     #Feature 2 Integration Tests
#     def test1_add_results(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       students = [student1.username, student2.username, student3.username]
#       team = add_team(mod.username, comp.name, "Runtime Terrors", students)
#       comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
#       assert comp_team.points_earned == 15
    
#     def test2_add_results(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       student4 = create_student("mark", "markpass")
#       student5 = create_student("eric", "ericpass")
#       students = [student1.username, student2.username, student3.username]
#       add_team(mod.username, comp.name, "Runtime Terrors", students)
#       comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
#       students = [student1.username, student4.username, student5.username]
#       team = add_team(mod.username, comp.name, "Scrum Lords", students)
#       assert team == None
    
#     def test3_add_results(self):
#       db.drop_all()
#       db.create_all()
#       mod1 = create_moderator("debra", "debrapass")
#       mod2 = create_moderator("robert", "robertpass")
#       comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       students = [student1.username, student2.username, student3.username]
#       team = add_team(mod2.username, comp.name, "Runtime Terrors", students)
#       assert team == None

#     #Feature 3 Integration Tests
#     def test_display_student_info(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       students = [student1.username, student2.username, student3.username]
#       team = add_team(mod.username, comp.name, "Runtime Terrors", students)
#       comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
#       update_ratings(mod.username, comp.name)
#       update_rankings(comp)
#       self.assertDictEqual(display_student_info("james"), {"profile": {'id': 1, 'username': 'james', 'rating_score': 24.0, 'comp_count': 1, 'curr_rank': 1}, "competitions": ['RunTime']})

#     #Feature 4 Integration Tests
#     def test_display_competition(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       student4 = create_student("mark", "markpass")
#       student5 = create_student("eric", "ericpass")
#       student6 = create_student("ryan", "ryanpass")
#       student7 = create_student("isabella", "isabellapass")
#       student8 = create_student("richard", "richardpass")
#       student9 = create_student("jessica", "jessicapass")
#       students1 = [student1.username, student2.username, student3.username]
#       team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
#       comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
#       students2 = [student4.username, student5.username, student6.username]
#       team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
#       comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 12)
#       students3 = [student7.username, student8.username, student9.username]
#       team3 = add_team(mod.username, comp.name, "Beyond Infinity", students3)
#       comp_team = add_results(mod.username, comp.name, "Beyond Infinity", 10)
#       update_ratings(mod.username, comp.name)
#       update_rankings(comp)
#       self.assertDictEqual(comp.get_json(), {'id': 1, 'name': 'RunTime', 'date': '29-03-2024', 'location': 'St. Augustine', 'level': 2, 'max_score': 25, 'moderators': ['debra'], 'teams': ['Runtime Terrors', 'Scrum Lords', 'Beyond Infinity']})

#     #Feature 5 Integration Tests
#     def test_display_rankings(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       student4 = create_student("mark", "markpass")
#       student5 = create_student("eric", "ericpass")
#       student6 = create_student("ryan", "ryanpass")
#       students1 = [student1.username, student2.username, student3.username]
#       team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
#       comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
#       students2 = [student4.username, student5.username, student6.username]
#       team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
#       comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp.name)
#       update_rankings(comp)
#       self.assertListEqual(display_rankings(), [{"placement": 1, "student": "james", "rating score": 24.0}, {"placement": 1, "student": "steven", "rating score": 24.0}, {"placement": 1, "student": "emily", "rating score": 24.0}, {"placement": 4, "student": "mark", "rating score": 16.0}, {"placement": 4, "student": "eric", "rating score": 16.0}, {"placement": 4, "student": "ryan", "rating score": 16.0}])

#     #Feature 6 Integration Tests
#     def test1_display_notification(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       student4 = create_student("mark", "markpass")
#       student5 = create_student("eric", "ericpass")
#       student6 = create_student("ryan", "ryanpass")
#       students1 = [student1.username, student2.username, student3.username]
#       team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
#       comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
#       students2 = [student4.username, student5.username, student6.username]
#       team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
#       comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp.name)
#       update_rankings(comp)
#       self.assertDictEqual(display_notifications("james"), {"notifications": [{"ID": 1, "Notification": "RANK : 1. Congratulations on your first rank!"}]})

#     def test2_display_notification(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 30)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       student4 = create_student("mark", "markpass")
#       student5 = create_student("eric", "ericpass")
#       student6 = create_student("ryan", "ryanpass")
#       students1 = [student1.username, student2.username, student3.username]
#       team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
#       comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
#       students2 = [student4.username, student5.username, student6.username]
#       team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
#       comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp1.name)
#       update_rankings(comp1)
#       students3 = [student1.username, student4.username, student5.username]
#       team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
#       comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 15)
#       students4 = [student2.username, student3.username, student6.username]
#       team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
#       comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp2.name)
#       update_rankings(comp2)
#       self.assertDictEqual(display_notifications("james"), {"notifications": [{"ID": 1, "Notification": "RANK : 1. Congratulations on your first rank!"}, {"ID": 7, "Notification": "RANK : 1. Well done! You retained your rank."}]})

#     def test3_display_notification(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       student4 = create_student("mark", "markpass")
#       student5 = create_student("eric", "ericpass")
#       student6 = create_student("ryan", "ryanpass")
#       students1 = [student1.username, student2.username, student3.username]
#       team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
#       comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
#       students2 = [student4.username, student5.username, student6.username]
#       team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
#       comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp1.name)
#       update_rankings(comp1)
#       students3 = [student1.username, student4.username, student5.username]
#       team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
#       comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
#       students4 = [student2.username, student3.username, student6.username]
#       team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
#       comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp2.name)
#       update_rankings(comp2)
#       self.assertDictEqual(display_notifications("steven"), {"notifications": [{"ID": 2, "Notification": "RANK : 1. Congratulations on your first rank!"}, {"ID": 10, "Notification": "RANK : 4. Oh no! Your rank has went down."}]})

#     def test4_display_notification(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       student4 = create_student("mark", "markpass")
#       student5 = create_student("eric", "ericpass")
#       student6 = create_student("ryan", "ryanpass")
#       students1 = [student1.username, student2.username, student3.username]
#       team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
#       comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
#       students2 = [student4.username, student5.username, student6.username]
#       team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
#       comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp1.name)
#       update_rankings(comp1)
#       students3 = [student1.username, student4.username, student5.username]
#       team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
#       comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
#       students4 = [student2.username, student3.username, student6.username]
#       team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
#       comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp2.name)
#       update_rankings(comp2)
#       self.assertDictEqual(display_notifications("mark"), {"notifications": [{"ID": 4, "Notification": "RANK : 4. Congratulations on your first rank!"}, {"ID": 8, "Notification": "RANK : 2. Congratulations! Your rank has went up."}]})

    
#     def test_student_list(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       student4 = create_student("mark", "markpass")
#       student5 = create_student("eric", "ericpass")
#       student6 = create_student("ryan", "ryanpass")
#       students1 = [student1.username, student2.username, student3.username]
#       team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
#       comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
#       students2 = [student4.username, student5.username, student6.username]
#       team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
#       comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp1.name)
#       update_rankings(comp1)
#       students3 = [student1.username, student4.username, student5.username]
#       team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
#       comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
#       students4 = [student2.username, student3.username, student6.username]
#       team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
#       comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp2.name)
#       update_rankings(comp2)
#       self.assertEqual(get_all_students_json(), [{'id': 1, 'username': 'james', 'rating_score': 22, 'comp_count': 2, 'curr_rank': 1}, {'id': 2, 'username': 'steven', 'rating_score': 17, 'comp_count': 2, 'curr_rank': 4}, {'id': 3, 'username': 'emily', 'rating_score': 17, 'comp_count': 2, 'curr_rank': 4}, {'id': 4, 'username': 'mark', 'rating_score': 18, 'comp_count': 2, 'curr_rank': 2}, {'id': 5, 'username': 'eric', 'rating_score': 18, 'comp_count': 2, 'curr_rank': 2}, {'id': 6, 'username': 'ryan', 'rating_score': 13, 'comp_count': 2, 'curr_rank': 6}])

#     def test_comp_list(self):
#       db.drop_all()
#       db.create_all()
#       mod = create_moderator("debra", "debrapass")
#       comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
#       comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
#       student1 = create_student("james", "jamespass")
#       student2 = create_student("steven", "stevenpass")
#       student3 = create_student("emily", "emilypass")
#       student4 = create_student("mark", "markpass")
#       student5 = create_student("eric", "ericpass")
#       student6 = create_student("ryan", "ryanpass")
#       students1 = [student1.username, student2.username, student3.username]
#       team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
#       comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
#       students2 = [student4.username, student5.username, student6.username]
#       team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
#       comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp1.name)
#       update_rankings(comp1)
#       students3 = [student1.username, student4.username, student5.username]
#       team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
#       comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
#       students4 = [student2.username, student3.username, student6.username]
#       team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
#       comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
#       update_ratings(mod.username, comp2.name)
#       update_rankings(comp2)
#       self.assertListEqual(get_all_competitions_json(), [{"id": 1, "name": "RunTime", "date": "29-03-2024", "location": "St. Augustine", "level": 2, "max_score": 25, "moderators": ["debra"], "teams": ["Runtime Terrors", "Scrum Lords"]}, {"id": 2, "name": "Hacker Cup", "date": "23-02-2024", "location": "Macoya", "level": 1, "max_score": 20, "moderators": ["debra"], "teams": ["Runtime Terrors", "Scrum Lords"]}])