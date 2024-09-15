from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# list exercise
# days - exercise too
# sets per exercise
# rep range
# progression: "beginner" | "intermediate" | "advanced"
class Split(models.Model):
	'''Example:
	user = 'manuel_test'
	exercises = 'lat_pulldown,preacher_curls,barbell_bench_press,shoulder_press,leg_curl'
	days = 'SMTWHFA'
	exercises_performed_on_day = 'SW,SW,MH,MH,TF'
	sets_per_exercise = '3,3,3,3,3'
	rep_range = 'low'
	progression = 'beginner'
	'''
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='split', null=True)
	exercises = models.CharField(max_length=1000)
	days = models.CharField(max_length=7)
	exercises_performed_on_day = models.CharField(max_length=1000, null=True)
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
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='past_workouts', null=True)
	date = models.DateTimeField()
	exercises = models.CharField(max_length=1000)
	days = models.CharField(max_length=7)
	sets_per_exercise = models.CharField(max_length=100)
	reps = models.CharField(max_length=300)
	weight = models.CharField(max_length=500)
	
