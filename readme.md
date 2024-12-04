# *Competitions-Platform*
### Web Spasm Project

Maia Neptune
Danara Sahadeo
Jonathan Swamber
Zidane Timothy

# Web Application Introduction
Time to show off your rank and rating over time to your friends and colleagues. Introducing our one-stop platform for recording, moderating and uploading  all your competition needs. This tailor-made competition platform was developed to assist Students, lecturers and Mooderators in officiating all your students' competitions!

# Project Summary
This is a COMP3613 Software Engineering II Project designed to be an online platform for managing and viewing students' competitions over time while allowing moderators to create and officiate competition results. Guest without an account can view the results of competitions as well as the students/teams that took part in them. They can also view students' progress in rank by navigating from their names. Moderators can: create competitions, determine the scores earned and add teams of students to these competitions. They can also view student progress. Students can view their progress as they traverse the ranks via notification viewing, calendar tracking and graph views of their rank per update by date. This platform fulfils the needs of a competition platform for students, moderators, and onlookers. 

Flask MVC Template
A template for flask applications structured in the Model View Controller pattern Demo. Postman Collection

Dependencies
Python3/pip3
Packages listed in requirements.txt
Installing Dependencies
$ pip install -r requirements.txt
Configuration Management
Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories. Instead, all config is provided by a config file or via environment variables.

In Development
When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py

SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
These values would be imported and added to the app in load_config() function in config.py

config.py

# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
In Production
When deploying your application to production/staging you must pass in configuration information via environment tab of your render project's dashboard.

perms

Flask Commands
wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. You just need create a manager command function, for example:

# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli
Then execute the command invoking with flask cli with command name and the relevant parameters

$ flask user create bob bobpass
Running the Project
For development run the serve command (what you execute):

$ flask run
For production using gunicorn (what heroku executes):

$ gunicorn wsgi:app
Deploying
You can deploy your version of this app to heroku by clicking on the "Deploy to heroku" link above.

Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

$ flask init
Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models. Then execute following commands using manage.py. More info here

$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help

Testing
Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
You can then execute all user tests as follows

$ flask test app
You can also supply "unit" or "int" at the end of the command to execute only unit or integration tests.

You can run all application tests with the following command

$ pytest
Test Coverage
You can generate a report on your test coverage via the following command

$ coverage report
You can also generate a detailed html report in a directory named htmlcov with the following comand

$ coverage html
Troubleshooting
Views 404ing
If your newly created views are returning 404 ensure that they are added to the list in main.py.

from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
Cannot Update Workflow file
If you are running into errors in gitpod when updateding your github actions file, ensure your github permissions in gitpod has workflow enabled perms

Database Issues
If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
