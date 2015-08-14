from django.db import models

# Create your models here.
class Match(models.Model):
    match_id = models.IntegerField()
    region = models.CharField(max_length=3)
    data = models.TextField()