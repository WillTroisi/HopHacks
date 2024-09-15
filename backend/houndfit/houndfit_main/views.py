from dataclasses import dataclass

from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Split, PastWorkouts
from .obj_list_convert import convert_object_list_to_split
from .forms import SplitBuilderForm
from .get_exercises import get_filtered_exercises


class SplitBuilderView(LoginRequiredMixin, generic.FormView):
	template_name = "houndfit_main/split_builder_view_user.html"	
	form_class = SplitBuilderForm
	success_url = '/'

	def form_valid(self, form):
		workout_days = form.cleaned_data['workout_days'] # ex: ["S", "T", "F"]
		experience = form.cleaned_data['experience_level'] # ex: "beginner"

		# create split here

		frequency = len(workout_days)
		exercises = ""
		days = ''.join(workout_days)
		exercises_performed_on_days = ""
		sets_per_exercise = ""
		rep_range = ""
		progression = experience

		chest_exercises = get_filtered_exercises("chest", experience, "compound", "barbell")
		shoulder_exercises = get_filtered_exercises("shoulders", experience, "compound", "cable")
		tricep_exercises = get_filtered_exercises("triceps", experience, "isolation", "cable")

		middle_back_exercises = get_filtered_exercises("middle back", experience, "compound", "barbell")
		bicep_exercises = get_filtered_exercises("biceps", experience, "isolation", "machine")

		quads_exercises = get_filtered_exercises("quadriceps", experience, "compound", "barbell")
		hamstrings_exercises = get_filtered_exercises("hamstrings", experience, "compound", "barbell")

		if frequency <= 3:
			exercises += chest_exercises[0]['id'] + ','
			exercises += shoulder_exercises[0]['id'] + ','
			exercises += middle_back_exercises[0]['id'] + ','
			exercises += quads_exercises[0]['id'] + ','
			exercises += hamstrings_exercises[0]['id']

			for x in range(frequency):
				exercises_performed_on_days += days + ','
			sets_per_exercise = '3,3,3,3,3'

		elif frequency == 4 or frequency == 5:
			# upper 
			exercises += chest_exercises[0]['id'] + ','
			exercises += shoulder_exercises[0]['id'] + ','

			exercises += middle_back_exercises[0]['id'] + ','
			exercises += middle_back_exercises[1]['id'] + ','

			exercises += bicep_exercises[0]['id'] + ','
			exercises += tricep_exercises[0]['id'] + ','

			# lower
			exercises += quads_exercises[0]['id'] + ','
			exercises += hamstrings_exercises[0]['id']

			# ex
			# exercises = 'bench_press,wide_grip_bench_press,barbell_row,lat_pulldown,preacher_curl,tricep_pushdown,squats,leg_curl
			# days = "SMTW"
			# exercises_performed_on_days = 'ST,ST,ST,ST,ST,ST,MW,MW'
			
			temp_exercises = [''] * 8
			adding_upper = True
			for day in days:
				if adding_upper:
					for x in range(6):
						temp_exercises[x] += day
					adding_upper = False
				else:
					temp_exercises[6] += day
					temp_exercises[7] += day
					adding_upper = True
			exercises_performed_on_days = ','.join(temp_exercises)
			sets_per_exercise = '3,3,3,3,2,2,3,3'
		elif frequency == 6:
			# ppl
			exercises += chest_exercises[0]['id'] + ',' # 0
			exercises += chest_exercises[1]['id'] + ',' # 1
			exercises += shoulder_exercises[0]['id'] + ',' # 2
			exercises += shoulder_exercises[1]['id'] + ',' # 3
			exercises += tricep_exercises[0]['id'] + ',' # 4


			exercises += middle_back_exercises[0]['id'] + ',' # 5
			exercises += middle_back_exercises[1]['id'] + ',' # 6
			exercises += bicep_exercises[0]['id'] + ',' # 7 
			exercises += bicep_exercises[1]['id'] + ',' # 8

			# lower
			exercises += quads_exercises[0]['id'] + ',' # 9 
			exercises += hamstrings_exercises[0]['id'] # 10

			temp_exercises = [''] * 11
			ppl_counter = 0
			for day in days:
				print(f'day {day}')
				if ppl_counter == 0:
					for x in range(5):
						temp_exercises[x] += day
					ppl_counter+=1
				elif ppl_counter == 1:
					for x in range(5,9):
						temp_exercises[x] += day
					ppl_counter += 1
				elif ppl_counter == 2:
					temp_exercises[9] += day
					temp_exercises[10] += day
					ppl_counter == 0
			print(temp_exercises)
			exercises_performed_on_days = ','.join(temp_exercises)
			sets_per_exercise = '3,3,3,3,3,3,3,3,3,3,3'
					


		if progression == 'beginner':
			rep_range = 'med'
		elif progression == 'intermediate':
			rep_range = 'med'
		elif progression == 'advanced':
			rep_range = 'low'
	
		print(self.request.user)
		print(exercises)
		print(days)
		print(exercises_performed_on_days)
		print(sets_per_exercise)
		print(rep_range)
		print(progression)


		s = Split(
			user=self.request.user, 
			exercises=exercises, days=days,
			exercises_performed_on_day=exercises_performed_on_days,
			sets_per_exercise=sets_per_exercise, 
			rep_range=rep_range, 
			progression=progression
			)
		s.save()
		return super().form_valid(form)

class SplitUserListView(LoginRequiredMixin, generic.ListView):
	model = Split
	context_object_name = 'split'
	template_name = 'houndfit_main/split_view_user.html'

	def get_queryset(self):
		return (
			Split.objects.filter(user=self.request.user)
		)

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		all_splits = self.object_list
		if all_splits.count() != 0:
			data['split_info'] = convert_object_list_to_split(all_splits)
		return data

class PastWorkoutUserListView(LoginRequiredMixin, generic.ListView):
	model = PastWorkouts
	context_object_name = 'past_workouts'
	template_name = 'houndfit_main/past_workouts_user.html'

	def get_queryset(self):
		return (
			PastWorkouts.objects.filter(user=self.request.user)
		)

def index(request):
	return render(request, 'base.html', {})

def registerpage(request):
	if request.method == 'GET':
		form = UserCreationForm()
		context = {'form': form}
		return render(request, template_name='registration/register.html', context=context)
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/houndfit_main')
		else:
			return redirect('register')

@login_required
def data(request):
	return HttpResponse("View volume data")

