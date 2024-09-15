from django import forms

days_to_the_gym = (
	("SUN", "S"),
	("MON", "M"),
	("TUES", "T"),
	("WED", "W"),
	("THUR", "H"),
	("FRI", "F"),
	("SAT", "A"),

)

experience_levels = (
	("beginner", "Beginner"),
	("intermediate", "Intermediate"),
	("advanced", "Advanced")
)

class SplitBuilderForm(forms.Form):
	workout_days = forms.MultipleChoiceField(choices=days_to_the_gym)
	experience_level = forms.ChoiceField(choices=experience_levels)
