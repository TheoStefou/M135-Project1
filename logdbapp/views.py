from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.db import connection

from .forms import LoginForm, SignupForm, FromToForm, FromToTypeForm, DateForm, IPForm, AccessLogForm, DataxceiverLogForm, NamesystemLogForm

from django.contrib.auth.models import User
from .models import User_Address, Log, Access_Arguments, Dataxceiver_Arguments, Namesystem_Blocks, Namesystem_Destinations, User_History

import datetime

class StoredFunction1(LoginRequiredMixin, View):

	login_url = '/logdb/login/'

	def get(self, request):

		form = FromToForm()
		context = {
			'form' : form,
			'has_results' : False,
			'date_format_error' : False
		}

		return render(request, 'logdbapp/storedfunction1.html', context)

	def post(self, request):

		dates = request.POST.dict()
		_from = dates.get("_from")
		to = dates.get("to")
		date_format_error = False

		form = FromToForm()
		context = {
			'form' : form,
			'has_results' : False
		}
		with connection.cursor() as cursor:

			try:
				cursor.execute("SELECT * FROM logdb.stored_function1(%s,%s);", [_from, to])
				results = cursor.fetchall()
				context['results'] = results
				context['has_results'] = True
				context['date_format_error'] = False
				add_to_user_history(request.user.username, 'stored_function1({},{})'.format(_from, to))
					
			except:
				context['date_format_error'] = True
				context['form'] = FromToForm(request.POST)
			
		return render(request, 'logdbapp/storedfunction1.html', context)

class StoredFunction2(LoginRequiredMixin, View):

	login_url = '/logdb/login/'

	def get(self, request):

		form = FromToTypeForm()
		context = {
			'form' : form,
			'has_results' : False
		}

		return render(request, 'logdbapp/storedfunction2.html', context)

	def post(self, request):

		data = request.POST.dict()
		_from = data.get("_from")
		to = data.get("to")
		type_choice = data.get("log_type")

		form = FromToTypeForm()
		context = {
				'form' : form,
				'has_results' : False

			}
		
		with connection.cursor() as cursor:
			try:
				cursor.execute("SELECT * FROM logdb.stored_function2(%s,%s,%s);", [type_choice, _from, to])
				results = cursor.fetchall()
				context['results'] = results
				context['has_results'] = True
				context['date_format_error'] = False
				add_to_user_history(request.user.username, 'stored_function2({},{}, {})'.format(type_choice, _from, to))
			except:
				context['date_format_error'] = True
				context['form'] = FromToTypeForm(request.POST)

		return render(request, 'logdbapp/storedfunction2.html', context)

class StoredFunction3(LoginRequiredMixin, View):

	login_url = '/logdb/login/'

	def get(self, request):

		form = DateForm()
		context = {
			'form' : form,
			'has_results' : False
		}

		return render(request, 'logdbapp/storedfunction3.html', context)

	def post(self, request):

		data = request.POST.dict()
		day = data.get("day")

		form = DateForm()
		context = {
				'form' : form,
				'has_results' : False

			}
		
		with connection.cursor() as cursor:
			try:
				cursor.execute("SELECT * FROM logdb.stored_function3(%s);", [day])
				results = cursor.fetchall()
				context['results'] = results
				context['has_results'] = True
				context['date_format_error'] = False
				add_to_user_history(request.user.username, 'stored_function3({})'.format(day))
			except:
				context['date_format_error'] = True
				context['form'] = DateForm(request.POST)

		return render(request, 'logdbapp/storedfunction3.html', context)

class SearchBySourceIp(LoginRequiredMixin, View):

	login_url = '/logdb/login/'

	def get(self, request):

		form = IPForm()
		context = {
			'form' : form,
			'has_results' : False
		}

		return render(request, 'logdbapp/searchbasedonip.html', context)

	def post(self, request):

		data = request.POST.dict()
		ip = data.get("source_ip")

		form = IPForm()
		context = {
				'form' : form,
				'has_results' : False

			}
		
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM logdb.search_based_on_ip(%s);", [ip])
			results = cursor.fetchall()
			context['results'] = results
			context['has_results'] = True
			add_to_user_history(request.user.username, 'search_based_on_ip({})'.format(ip))

		return render(request, 'logdbapp/searchbasedonip.html', context)

class NewLog(LoginRequiredMixin, View):
	
	login_url = '/logdb/login'

	def get(self, request):

		return render(request, 'logdbapp/newlog.html', {})

class NewAccessLog(LoginRequiredMixin, View):

	login_url = '/logdb/login'

	def get(self, request):

		form = AccessLogForm()
		context = {
			'form' : form,
			'success' : False,
			'something_went_wrong' : False
		}
		return render(request, 'logdbapp/newaccesslog.html', context)

	def post(self, request):

		form = AccessLogForm()
		context = {}

		data = request.POST.dict()
		timestamp = data.get("timestamp")
		source_ip = data.get("source_ip")
		user_id = data.get("user_id")
		http_method = data.get("http_method")
		resource = data.get("resource")
		response = data.get("response")
		size = data.get("size")
		referer = data.get("referer")
		user_agent = data.get("user_agent")

		context['something_went_wrong'] = False
		context['success'] = False
		try:
			timestamp = datetime.datetime.strptime(timestamp, '%Y/%m/%d %H:%M:%S')
			int(response)
			int(size)
		except:
			context['form'] = AccessLogForm(request.POST)
			context['something_went_wrong'] = True
			context['success'] = False
			return render(request, 'logdbapp/newaccesslog.html', context)

		#Data is ready to be inserted
		log = Log.objects.create(log_timestamp=timestamp, log_type='access', source_ip=source_ip)
		log.save()
		access_args = Access_Arguments.objects.create(	access_arguments_log=log,
														access_arguments_user_id=user_id,
														access_arguments_http_method=http_method,
														access_arguments_resource=resource,
														access_arguments_response=response,
														access_arguments_size=size,
														access_arguments_referer=referer,
														access_arguments_agent_string=user_agent)
		access_args.save()
		context['success'] = True
		context['form'] = AccessLogForm()
		add_to_user_history(request.user.username, 'insert access log {}'.format(log.log_id))
		return render(request, 'logdbapp/newaccesslog.html', context)

class NewDataxceiverLog(LoginRequiredMixin, View):
	
	login_url = '/logdb/login'

	def get(self, request):
		form = DataxceiverLogForm()
		context = {
			'form' : form,
			'success' : False,
			'something_went_wrong' : False
		}
		return render(request, 'logdbapp/newdataxceiverlog.html', context)

	def post(self, request):

		context = {}

		data = request.POST.dict()
		timestamp = data.get("timestamp")
		source_ip = data.get("source_ip")
		block_id = data.get("block_id")
		dest_ip = data.get("dest_ip")
		size = data.get("size")
		typ = data.get("typ")

		context['something_went_wrong'] = False
		context['success'] = False
		try:
			timestamp = datetime.datetime.strptime(timestamp, '%Y/%m/%d %H:%M:%S')
			if size == '':
				size = None
			else:
				size = int(size)
		except:
			context['form'] = DataxceiverLogForm(request.POST)
			context['something_went_wrong'] = True
			context['success'] = False
			return render(request, 'logdbapp/newdataxceiverlog.html', context)

		#Data is ready to be inserted
		log = Log.objects.create(log_timestamp=timestamp, log_type=typ, source_ip=source_ip)
		log.save()
		access_args = Dataxceiver_Arguments.objects.create(	dataxceiver_arguments_log=log,
															dataxceiver_arguments_block_id=block_id,
															dataxceiver_arguments_dest_ip=dest_ip,
															dataxceiver_arguments_size=size)
		access_args.save()
		context['success'] = True
		context['form'] = DataxceiverLogForm()
		add_to_user_history(request.user.username, 'insert dataxceiver log {}'.format(log.log_id))
		return render(request, 'logdbapp/newaccesslog.html', context)



class NewNamesystemLog(LoginRequiredMixin, View):
	
	login_url = '/logdb/login/'

	def get(self, request):

		form = NamesystemLogForm()
		context = {
			'form' : form
		}
		return render(request, 'logdbapp/newnamesystemlog.html', context)

	def post(self, request):

		context = {}

		data = request.POST.dict()
		timestamp = data.get("timestamp")
		source_ip = data.get("source_ip")
		typ = data.get("typ")
		blocks = data.get("blocks").split()
		destinations = data.get("destinations").split()

		context['something_went_wrong'] = False
		context['success'] = False
		try:
			timestamp = datetime.datetime.strptime(timestamp, '%Y/%m/%d %H:%M:%S')
		except:
			context['form'] = NamesystemLogForm(request.POST)
			context['something_went_wrong'] = True
			context['success'] = False
			return render(request, 'logdbapp/newnameystemlog.html', context)

		#Data is ready to be inserted
		log = Log.objects.create(log_timestamp=timestamp, log_type=typ, source_ip=source_ip)
		log.save()
		
		for block in blocks:
			namesystem_blocks_entry = Namesystem_Blocks.objects.create(	namesystem_blocks_log=log,
																		namesystem_blocks_block_id=block)
			namesystem_blocks_entry.save()

		for destination in destinations:
			namesystem_destinations_entry = Namesystem_Destinations.objects.create(	namesystem_destinations_log=log,
																		namesystem_destinations_dest_ip=block)
			namesystem_destinations_entry.save()

		context['success'] = True
		context['form'] = DataxceiverLogForm()
		add_to_user_history(request.user.username, 'insert namesystem log {}'.format(log.log_id))
		return render(request, 'logdbapp/newnamesystemlog.html', context)

class Profile(LoginRequiredMixin, View):

	login_url = '/logdb/login/'

	def get(self, request):

		user = request.user
		address = User_Address.objects.get(pk=user)

		context = {
			'user' : user,
			'address' : address.address
		}

		return render(request, 'logdbapp/profile.html',context)

class Index(LoginRequiredMixin, View):

	login_url = '/logdb/login/'

	def get(self, request):
		context = {
			'user' : request.user
		}
		return render(request, 'logdbapp/index.html', context)

class Login(View):

	def get(self, request):
		
		if request.user.is_authenticated:
			return redirect('/logdb/')

		form = LoginForm()
		context = {
			'form' : form
		}
		return render(request, 'logdbapp/login.html', context)

	def post(self, request):

		if request.user.is_authenticated:
			return redirect('/logdb/')
		login_data 	= request.POST.dict()
		username 	= login_data.get("username")
		password 	= login_data.get("password")
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/logdb/')
		
		form = LoginForm()
		context = {
			'form' : form,
			'retry' : True
		}
		return render(request, 'logdbapp/login.html', context)

class Logout(View):

	def get(self, request):
		logout(request)
		return redirect('/logdb/login/')

class Signup(View):

	def user_exists(self, username):
		try:
			User.objects.get(username=username)
			return True
		except:
			return False


	def get(self, request):
		if request.user.is_authenticated:
			return redirect('/logdb/')
		form = SignupForm()
		context = {
			'form' : form
		}
		return render(request, 'logdbapp/signup.html', context)

	def post(self, request):

		if request.user.is_authenticated:
			return redirect('/logdb/')
		signup_data = request.POST.dict()
		firstname = signup_data.get("firstname")
		lastname = signup_data.get("lastname")
		username = signup_data.get("username")
		email = signup_data.get("email")
		password1 = signup_data.get("password1")
		password2 = signup_data.get("password2")
		address = signup_data.get("address")

		user_already_exists = self.user_exists(username)

		if password1 != password2:
			form = SignupForm()
			context = {
				'form' : form,
				'no_match' : True,
				'ok' : False,
				'already_exists' : False

			}
			return render(request, 'logdbapp/signup.html', context)
		elif user_already_exists:
			form = SignupForm(request.POST)
			context = {
				'form' : form,
				'no_match' : False,
				'ok' : False,
				'already_exists' : True

			}
			return render(request, 'logdbapp/signup.html', context)
		else:
			user = User.objects.create_user(username, email, password1)
			user.is_active = True
			user.first_name = firstname
			user.last_name = lastname
			user.save()

			address = User_Address(user_id=user, address=address)
			address.save()

			form = SignupForm()
			context = {
				'form' : form,
				'no_match' : False,
				'ok' : True,
				'already_exists' : False

			}
			return render(request, 'logdbapp/signup.html', context)


def add_to_user_history(username, action):
	user_history = User_History.objects.create(user_history_username=username, user_history_action=action)
	user_history.save()