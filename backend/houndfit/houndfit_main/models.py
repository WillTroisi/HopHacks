from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Split(models.Model):
	# list exercise
	# days - exercise too
	# sets per exercise
	# rep range
	# progression: "beginner" | "intermediate" | "advanced"
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='split', null=True)
	exercises = models.CharField(max_length=1000)
	days = models.CharField(max_length=7)
	sets_per_exercise = models.CharField(max_length=100)
	rep_range = models.CharField(max_length=10)
	progression = models.CharField(max_length=15)


class PastWorkouts(models.Model):
	# start time
	# end time
	# date
	# workout
	# sets
	# reps
	# weight
	date = models.DateTimeField()
	exercises = models.CharField(max_length=1000)
	days = models.CharField(max_length=7)
	sets_per_exercise = models.CharField(max_length=100)
	reps = models.CharField(max_length=300)
	weight = models.CharField(max_length=500)
	
