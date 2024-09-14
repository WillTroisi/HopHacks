from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('split/', views.SplitUserListView.as_view(), name='split')
	# path('login/', views.loginpage, name='login'),
	# path('logout/', views.logoutpage, name='logout'),
	# path('register/', views.registerpage, name='register'),
]