import csv
import click, pytest, sys
from flask import Flask
from datetime import datetime, date

from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()

    #creates students
    with open("students.csv") as student_file:
        reader = csv.DictReader(student_file)

        for student in reader:
            stud = create_student(student['username'], student['password'])
            #db.session.add(stud)
        #db.session.commit()
    
    student_file.close()

    #creates moderators
    with open("moderators.csv") as moderator_file:
        reader = csv.DictReader(moderator_file)

        for moderator in reader:
            mod = create_moderator(moderator['username'], moderator['password'])
            #db.session.add(mod)
        #db.session.commit()
    
    moderator_file.close()

    #creates competitions
    with open("competitions.csv") as competition_file:
        reader = csv.DictReader(competition_file)

        for competition in reader:
            comp = create_competition(competition['mod_name'], competition['comp_name'], competition['date'], competition['location'], competition['level'], competition['max_score'])
    
    competition_file.close()
    
    with open("results.csv") as results_file:
        reader = csv.DictReader(results_file)

        for result in reader:
            students = [result['student1'], result['student2'], result['student3']]
            team = add_team(result['mod_name'], result['comp_name'], result['team_name'], students)
            add_results(result['mod_name'], result['comp_name'], result['team_name'], int(result['score']))
            #db.session.add(comp)
        #db.session.commit()
    
    results_file.close()

    with open("competitions.csv") as competitions_file:
        reader = csv.DictReader(competitions_file)
        
        for competition in reader:
            if competition['comp_name'] != 'TopCoder':
                update_ratings(competition['mod_name'], competition['comp_name'])
                competition_query = Competition.query.filter_by(name=competition['comp_name']).first()
                update_rankings(competition_query)
            #db.session.add(comp)
        #db.session.commit()
    
    competitions_file.close()

    """
    stud1 = create_student('stud1', 'stud1pass')
    stud2 = create_student('stud2', 'stud2pass')
    stud3 = create_student('stud3', 'stud3pass')
    stud4 = create_student('stud4', 'stud4pass')
    stud5 = create_student('stud5', 'stud5pass')
    stud6 = create_student('stud6', 'stud6pass')
    stud7 = create_student('stud7', 'stud7pass')
    stud8 = create_student('stud8', 'stud8pass')
    stud9 = create_student('stud9', 'stud9pass')
    stud10 = create_student('stud10', 'stud10pass')
    mod1 = create_moderator('mod1', 'mod1pass')
    mod2 = create_moderator('mod2', 'mod2pass')
    mod3 = create_moderator('mod3', 'mod3pass')
    comp1 = create_competition('mod1', 'comp1', '09-02-2024', 'CSL', 1, 25)
    comp2 = create_competition('mod2', 'comp2', '09-02-2024', 'CSL', 2, 20)
    mod = add_mod('mod1', 'comp1', 'mod3')

    students = ["stud1", "stud2", "stud3"]
    add_team('mod1', 'comp1', "team1", students)
    add_results('mod1', 'comp1', "team1", 16)
    
    students = ["stud4", "stud5", "stud6"]
    add_team('mod1', 'comp1', "team2", students)
    add_results('mod1', 'comp1', "team2", 15)

    students = ["stud7", "stud8", "stud9"]
    add_team('mod1', 'comp1', "team3", students)
    add_results('mod1', 'comp1', "team3", 12)

    students = ["stud10", "stud4", "stud7"]
    add_team('mod2', 'comp2', "team1", students)
    add_results('mod2', 'comp2', "team1", 10)
    
    students = ["stud2", "stud5", "stud8"]
    add_team('mod2', 'comp2', "team2", students)
    add_results('mod2', 'comp2', "team2", 15)

    students = ["stud3", "stud6", "stud9"]
    add_team('mod2', 'comp2', "team3", students)
    add_results('mod2', 'comp2', "team3", 12)

    update_ratings('mod1', 'comp1')
    update_rankings()
    
    update_ratings('mod2', 'comp2')
    update_rankings()
    """
    print('database intialized')

'''
Student Commands
'''

student_cli = AppGroup("student", help="Student commands") 

@student_cli.command("create", help="Creates a student")
@click.argument("username", default="stud1")
@click.argument("password", default="stud1pass")
def create_student_command(username, password):
    student = create_student(username, password)

@student_cli.command("update", help="Updates a student's username")
@click.argument("id", default="1")
@click.argument("username", default="stud1")
def update_student_command(id, username):
    student = update_student(id, username)

@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_students_command(format):
    if format == 'string':
        print(get_all_students())
    else:
        print(get_all_students_json())

@student_cli.command("display", help="Displays student profile")
@click.argument("username", default="stud1")
def display_student_info_command(username):
    print(display_student_info(username))

@student_cli.command("notifications", help="Gets all notifications")
@click.argument("username", default="stud1")
def display_notifications_command(username):
    print(display_notifications(username))

app.cli.add_command(student_cli)


'''
Moderator Commands
'''

mod_cli = AppGroup("mod", help="Moderator commands") 

@mod_cli.command("create", help="Creates a moderator")
@click.argument("username", default="mod1")
@click.argument("password", default="mod1pass")
def create_moderator_command(username, password):
    mod = create_moderator(username, password)

@mod_cli.command("addMod", help="Adds a moderator to a competition")
@click.argument("mod1_name", default="mod1")
@click.argument("comp_name", default="comp1")
@click.argument("mod2_name", default="mod2")
def add_mod_to_comp_command(mod1_name, comp_name, mod2_name):
    mod = add_mod(mod1_name, comp_name, mod2_name)

"""
@mod_cli.command("addTeam", help="Adds a team to a competition")
@click.argument("mod_name", default="mod1")
@click.argument("comp_name", default="comp1")
@click.argument("team_name", default="A")
@click.argument("student1", default="stud1")
@click.argument("student2", default="stud2")
@click.argument("student3", default="stud3")
def add_team_to_comp_command(mod_name, comp_name, team_name, student1, student2, student3):
    students = [student1, student2, student3]
    comp = add_team(mod_name, comp_name, team_name, students)
"""

@mod_cli.command("addResults", help="Adds results for a team in a competition")
@click.argument("mod_name", default="mod1")
@click.argument("comp_name", default="comp1")
@click.argument("team_name", default="team1")
@click.argument("student1", default="stud1")
@click.argument("student2", default="stud2")
@click.argument("student3", default="stud3")
@click.argument("score", default=10)
def add_results_command(mod_name, comp_name, team_name, student1, student2, student3, score):
    students = [student1, student2, student3]
    comp = add_team(mod_name, comp_name, team_name, students)

    if comp:
        comp_team = add_results(mod_name, comp_name, team_name, score)

@mod_cli.command("confirm", help="Confirms results for all teams in a competition")
@click.argument("mod_name", default="mod1")
@click.argument("comp_name", default="comp1")
def update_rankings_command(mod_name, comp_name):
    update_ratings(mod_name, comp_name)
    comp = Competition.query.filter_by(name = comp_name).first()
    update_rankings(comp)

@mod_cli.command("rankings", help="Displays overall rankings")
def display_rankings_command():
    display_rankings()

@mod_cli.command("list", help="Lists moderators in the database")
@click.argument("format", default="string")
def list_moderators_command(format):
    if format == 'string':
        print(get_all_moderators())
    else:
        print(get_all_moderators_json())

app.cli.add_command(mod_cli)


'''
Competition commands
'''

comp_cli = AppGroup("comp", help = "Competition commands")   

@comp_cli.command("create", help = "Creates a competition")
@click.argument("mod_name", default = "mod1")
@click.argument("name", default = "comp1")
@click.argument("date", default = "09-02-2024")
@click.argument("location", default = "CSL")
@click.argument("level", default = 1)
@click.argument("max_score", default = 25)
def create_competition_command(mod_name, name, date, location, level, max_score):
    comp = create_competition(mod_name, name, date, location, level, max_score)

@comp_cli.command("details", help = "Displays competition details")
@click.argument("name", default = "comp1")
def display_competition_details_command(name):
    comp = get_competition_by_name(name)
    print(comp.get_json())

@comp_cli.command("list", help = "list all competitions")
def list_competition_command():
    print(get_all_competitions_json())

@comp_cli.command("results", help = "displays competition results")
@click.argument("name", default = "comp1")
def display_competition_results_command(name):
    print(display_competition_results(name))

app.cli.add_command(comp_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("app", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "IntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)

