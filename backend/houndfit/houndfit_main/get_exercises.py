import json

def _load_exercises_to_json(filename='exercises.json'):
	all_exercises_json = None
	with open(filename) as f:
		all_exercises_json = json.load(f)

	if all_exercises_json is None:
		raise Exception('Couldn\'t open exercises')
	return all_exercises_json

def get_filtered_exercises(primary_muscle, experience_level, joint_type, equipment):
	all_exercises_json = _load_exercises_to_json()
	return [x for x in all_exercises_json if primary_muscle in x['primaryMuscles'] 
		 													and x['level'] == experience_level 
															and x['mechanic'] == joint_type
															and x['equipment'] == equipment
															]


def convert_exercise_id_to_readable(exercise_id):
	all_exercises_json = _load_exercises_to_json()
	for exercise in all_exercises_json:
		if exercise['id'] == exercise_id:
			return exercise['name']
	return ""

