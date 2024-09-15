import json

def filter_exercises(primary_muscle, experience_level, joint_type, equipment):
	all_exercises_json = None
	with open('exercises.json') as f:
		all_exercises_json = json.load(f)

	if all_exercises_json is None:
		raise Exception('Couldn\'t open exercises')

	return [x for x in all_exercises_json if primary_muscle in x['primaryMuscles'] 
		 													and x['level'] == experience_level 
															and x['mechanic'] == joint_type
															and x['equipment'] == equipment
															]