from django.db import models

# Create your models here.
class Match(models.Model):
    match_id = models.IntegerField()
    region = models.CharField(max_length=3)
    version = models.CharField(max_length=4)
    gamemode = models.CharField(max_length=11)
    data = models.TextField()