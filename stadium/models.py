from django.db import models
# Create your models here.

class showcity(models.Model):
    city = models.CharField(max_length = 30)
    class Meta:
        db_table = "stadium_stadium"
class showmatch(models.Model):
    name = models.CharField(max_length = 100)
    date = models.DateField()
    city = models.CharField(max_length = 30)
    match_id = models.IntegerField(primary_key = True)
    game = models.CharField(max_length = 30)
    class Meta:
        db_table = "stadium_matches"
class showsnack(models.Model):
    snacks_id = models.IntegerField(primary_key = True)
    snacks = models.CharField(max_length = 50)
    price = models.IntegerField()
    class Meta:
        db_table = "stadium_snacks"
class Meta:
    db_table = "stadium_ticket"