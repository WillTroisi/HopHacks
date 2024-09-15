from django import forms

days_to_the_gym = (
	("S", "Sunday"),
	("M", "Monday"),
	("T", "Tuesday"),
	("W", "Wednesday"),
	("H", "Thursday"),
	("F", "Friday"),
	("A", "Saturday"),

)

experience_levels = (
	("beginner", "Beginner"),
	("intermediate", "Intermediate"),
	("advanced", "Advanced")
)

class SplitBuilderForm(forms.Form):
	workout_days = forms.MultipleChoiceField(choices=days_to_the_gym)
	experience_level = forms.ChoiceField(choices=experience_levels)
