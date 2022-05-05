from django.db import models
# Create your models here.

class snacks(models.Model):
    snacks_id = models.IntegerField(primary_key = True)
    snacks = models.CharField(max_length = 50)
    price = models.IntegerField()

class stadium(models.Model):
    stadium_id = models.IntegerField(primary_key = True)
    game = models.CharField(max_length = 30)
    name = models.CharField(max_length = 50)
    city = models.CharField(max_length = 30)
    pin = models.IntegerField()
    rent = models.IntegerField()

class matches(models.Model):
    match_id = models.IntegerField(primary_key = True)
    game = models.CharField(max_length = 30)
    name = models.CharField(max_length = 100)
    stadium = models.CharField(max_length = 50)
    stadium_id = models.IntegerField()
    city = models.CharField(max_length = 30)
    date = models.DateField()
    time = models.TimeField()

class seats(models.Model):
    match_id = models.IntegerField()
    S1 = models.IntegerField()
    S2 = models.IntegerField()
    S3 = models.IntegerField()
    S4 = models.IntegerField()
    S5 = models.IntegerField()
    S6 = models.IntegerField()
    S7 = models.IntegerField()
    S8 = models.IntegerField()
    S9 = models.IntegerField()
    S10 = models.IntegerField()

class book(models.Model):
    stadium_id = models.IntegerField()
    game = models.CharField(max_length = 30)
    name = models.CharField(max_length = 50)
    date = models.DateField()
    username = models.CharField(max_length = 50)
    city = models.CharField(max_length = 30)
    pin = models.IntegerField()
    rent = models.IntegerField()

class ticket(models.Model):
    ticket = models.CharField(max_length = 30, primary_key = True)
    username = models.CharField(max_length = 30)
    match_name = models.CharField(max_length = 30)
    match_id = models.IntegerField()
    stadium = models.CharField(max_length = 50)
    city = models.CharField(max_length = 30)
    date = models.DateField()
    time = models.TimeField()
    seat = models.IntegerField()
    price = models.IntegerField()
    snacks_id = models.IntegerField()
