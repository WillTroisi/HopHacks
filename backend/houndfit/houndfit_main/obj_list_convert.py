from datetime import datetime

from dataclasses import dataclass
from .models import Split, PastWorkouts
from django.db.models.query import QuerySet
from .get_exercises import convert_exercise_id_to_readable

@dataclass
class Exercise:
	name: str = None
	id: str = None
	sets: int = None
	reps: tuple[int,int] = None

@dataclass
class SplitRepresentation:
	exercises: list[Exercise] = None
	days: dict[str,Exercise] = None
	progression: str = None

@dataclass
class DiaryRepresentation:
	date: datetime = None
	sets: int = None
	weights: int = None


def convert_object_list_to_past_workouts(object_list: QuerySet[PastWorkouts]) -> list[DiaryRepresentation]:
	past_workouts = []
	for obj in object_list:
		sets = obj.sets_per_exercise.split(',')
		total_sets = 0
		for set_amount in sets:
			total_sets += int(set_amount)

		weights = obj.weight.split(',')
		total_weight = 0
		for weight in weights:
			total_weight += int(weight)
		
		date = obj.date
		past_workouts.append(DiaryRepresentation(date, total_sets, total_weight))
	return past_workouts

def convert_object_list_to_split(object_list: QuerySet[Split]) -> list[SplitRepresentation]:
	for obj in object_list:
		exercises = obj.exercises.split(',')
		exercises_performed_on_days = obj.exercises.split(',')
		exercises_sets = obj.sets_per_exercise.split(',')
		rep_description = obj.rep_range
		progression = obj.progression

		rep_range = None
		if rep_description == 'low':
			rep_range = (4,6)
		elif rep_description == 'high':
			rep_range = (12,20)
		else:
			rep_range = (8,12)

		exercises_data = []

		for i, exercise_id in enumerate(exercises):
			# conv to human readable name
			e = Exercise()
			e.name = convert_exercise_id_to_readable(exercise_id)
			e.id = exercise_id
			e.sets = exercises_sets[i]
			e.reps = rep_range
			exercises_data.append(e)
		days_and_exercises = {
			'S': [],
			'M': [],
			'T': [],
			'W': [],
			'H': [],
			'F': [],
			'A': [],
			}

		for i, days in enumerate(exercises_performed_on_days):
			for day in days:
				days_and_exercises[day] = exercises_data[i]
		return SplitRepresentation(exercises_data, days_and_exercises, progression)