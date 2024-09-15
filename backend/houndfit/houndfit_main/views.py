from dataclasses import dataclass

from django.db.models.query import QuerySet
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
		bicep_exercises = get_filtered_exercises("bicep", experience, "isolation", "cable")

		quads_exercises = get_filtered_exercises("quadriceps", experience, "compound", "barbell")
		hamstrings_exercises = get_filtered_exercises("hamstrings", experience, "compound", "barbell")

		if frequency <= 3:
			exercises += chest_exercises[0]['id'] + ','
			exercises += shoulder_exercises[0]['id'] + ','
			exercises += middle_back_exercises[0]['id'] + ','
			exercises += quads_exercises[0]['id'] + ','
			exercises += hamstrings_exercises[0]['id'] + ','

			for x in range(frequency):
				exercises_performed_on_days += days + ','
			sets_per_exercise = '3,3,3,3,3'

		elif frequency == 4:
			# upper 
			exercises += chest_exercises[0]['id'] + ','
			exercises += chest_exercises[1]['id'] + ','

			exercises += middle_back_exercises[0]['id'] + ','
			exercises += middle_back_exercises[1]['id'] + ','

			exercises += bicep_exercises[0]['id'] + ','
			exercises += tricep_exercises[0]['id'] + ','

			# lower
			exercises += quads_exercises[0]['id'] + ','
			exercises += hamstrings_exercises[0]['id'] + ','
			
			adding_upper = True
			for day in days:
				if adding_upper:
					exercises_performed_on_days += day * 6 + ','
					adding_upper = False



			...
		elif frequency == 5:
			# upper/lower + arm days
			...
		elif frequency == 6:
			# ppl
			...

		if progression == 'beginner':
			rep_range = 'med'
		elif progression == 'intermediate':
			rep_range = 'med'
		elif progression == 'advanced':
			rep_range = 'low'
		
		s = Split(self.request.user, exercises, days, exercises_performed_on_days, sets_per_exercise, rep_range, progression)

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
	return HttpResponse("Hello, world. Main view.")

def loginpage(request):
	if request.method == 'GET':
		return render(request, template_name='registration/login.html')
	
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			return redirect('login')

def logoutpage(request):
	...

def registerpage(request):
	if request.method == 'GET':
		return render(request, template_name='registration/register.html')
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('home')
		else:
			return redirect('register')

@login_required
def diary(request):
	return HttpResponse("Past Workouts")

@login_required
def split(request):
	return HttpResponse("Current Split")

@login_required
def split_builder(request):
	return HttpResponse("Build a split")

@login_required
def dashboard(request):
	return render(request, "users/dashboard.html")

@login_required
def data(request):
	return HttpResponse("View volume data")

# Create your views here.
