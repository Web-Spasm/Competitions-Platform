from App.database import db
from App.models import User
from abc import ABC, abstractmethod


@abstractmethod
def update_rank(self):
    pass