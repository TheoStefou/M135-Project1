from django.urls import path

from . import views

app_name = 'logdbapp'

urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('login/', views.Login.as_view(), name='login'),
	path('signup/', views.Signup.as_view(), name='signup'),
	path('logout/', views.Logout.as_view(), name='logout'),
	path('profile/', views.Profile.as_view(), name='profile'),
	path('storedfunction1/', views.StoredFunction1.as_view(), name='storedfunction1'),
	path('storedfunction2/', views.StoredFunction2.as_view(), name='storedfunction2'),
	path('storedfunction3/', views.StoredFunction3.as_view(), name='storedfunction3'),
	path('searchbyip/', views.SearchBySourceIp.as_view(), name='searchbyip'),


	path('new/', views.NewLog.as_view(), name='new'),
	path('new/access/', views.NewAccessLog.as_view(), name='newaccess'),
	path('new/dataxceiver/', views.NewDataxceiverLog.as_view(), name='newdataxceiver'),
	path('new/namesystem/', views.NewNamesystemLog.as_view(), name='newnamesystem'),
]