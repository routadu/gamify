from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Game(models.Model):

    gameID = models.AutoField(primary_key=True)
    displayName = models.CharField(
        max_length=30, default="", null=False, unique=True)
    minPlayingAge = models.IntegerField(default=5)
    description = models.CharField(max_length=200, default="")


class GameProgress(models.Model):

    username = models.CharField(
        max_length=20, null=False, default="")
    gameID = models.IntegerField(
        null=False, default=0)
    level: models.IntegerField(default=1, null=False)


class User(AbstractUser):

    username = models.CharField(
        max_length=20, unique=True, default="", null=False, primary_key=True)
    password = models.CharField(max_length=255, null=False, default="")
    name = models.CharField(max_length=50, default="", null=False)
    age = models.IntegerField(default=15)
    email = models.CharField(max_length=40, default="", unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'name', 'age', 'email']

    def fromAuthenticationDetails(username: str, passwordHash: str):
        user = User()
        user.username = username
        user.password = passwordHash

    def fromUserDetails(username: str, password: str, name: str, email: str, age: int):
        user = User()
        user.username = username
        user.password = password
        user.name = name
        user.email = email
        user.age = age
        return user

    def isUserEligibleForGame(self, game: Game) -> bool:
        return self.age >= game.minPlayingAge

    def isUserAdult(self) -> bool:
        return self.age >= 18

    def addPreferredGame(self, gameID: int):
        pass

    def getPreferredGames(self) -> list[int]:
        pass

    def __str__(self):
        return self.username
