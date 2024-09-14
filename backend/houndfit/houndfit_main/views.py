from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Split, PastWorkouts

class SplitUserListView(LoginRequiredMixin, generic.ListView):
	model = Split
	context_object_name = 'splits'
	template_name = 'houndfit_main/split_view_user.html'

	def get_queryset(self):
		return (
			Split.objects.filter(user=self.request.user)
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

def data(rqquest):
	return HttpResponse("View volume data")

# Create your views here.
