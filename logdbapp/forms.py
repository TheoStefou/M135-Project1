from django import forms

TYPE_CHOICES = [
	('access', 'access'),
	('receiving', 'receiving'),
	('received', 'received'),
	('served', 'served'),
	('remove', 'remove'),
	('replicate', 'replicate'),
]

HTTP_METHODS = [
	('GET', 'GET'),
	('POST', 'POST'),
	('HEAD', 'HEAD'),
	('PUT', 'PUT'),
	('DELETE', 'DELETE'),
	('CONNECT', 'CONNECT'),
	('OPTIONS', 'OPTIONS'),
	('TRACE', 'TRACE'),
	('PATCH', 'PATCH'),

]

DATAXCEIVER_TYPES = [
	('receiving', 'receiving'),
	('received', 'received'),
	('served', 'served'),
]

NAMESYSTEM_TYPES = [
	('replicate', 'replicate'),
	('delete', 'remove'),
	
]

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100)
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

class SignupForm(forms.Form):
	firstname 	= forms.CharField(label='Firstname', max_length=100)
	lastname 	= forms.CharField(label='Lastname', max_length=100)
	username 	= forms.CharField(label='Username', max_length=100)
	email 		= forms.EmailField()
	password1 	= forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput, error_messages={'required':''})
	password2 	= forms.CharField(label='Confirm Password', max_length=100, widget=forms.PasswordInput, error_messages={})
	address 	= forms.CharField(label='Address', max_length=100)

class FromToForm(forms.Form):
	_from = forms.CharField(label='From', max_length=19)
	to = forms.CharField(label='To', max_length=19)

class FromToTypeForm(forms.Form):
	_from 		= forms.CharField(label='From', max_length=19)
	to 			= forms.CharField(label='To', max_length=19)
	log_type 	= forms.MultipleChoiceField(widget=forms.RadioSelect, choices=TYPE_CHOICES)

class DateForm(forms.Form):
	day = forms.CharField(label='day', max_length=19)

class IPForm(forms.Form):
	source_ip 	= forms.CharField(label='source ip', max_length=50)

class AccessLogForm(forms.Form):
	timestamp 	= forms.CharField(label='timestamp', max_length=19)
	source_ip 	= forms.CharField(label='source ip', max_length=50)
	user_id 	= forms.CharField(label='user id', max_length=50)
	http_method = forms.ChoiceField(label='http method', choices=HTTP_METHODS)
	resource 	= forms.CharField(label='resource', max_length=2000)
	response 	= forms.CharField(label='response', max_length=50)
	size	 	= forms.CharField(label='size', max_length=50)
	referer 	= forms.CharField(label='referer', max_length=2000)
	user_agent	= forms.CharField(label='user agent string', max_length=2000)


class DataxceiverLogForm(forms.Form):
	timestamp 	= forms.CharField(label='timestamp', max_length=19)
	source_ip 	= forms.CharField(label='source ip', max_length=50)
	typ 		= forms.ChoiceField(label='type', choices=DATAXCEIVER_TYPES)
	block_id 	= forms.CharField(label='block id', max_length=50)
	dest_ip 	= forms.CharField(label='dest ip', max_length=50)
	size	 	= forms.CharField(label='size', max_length=20, required=False)

class NamesystemLogForm(forms.Form):
	timestamp 	= forms.CharField(label='timestamp', max_length=19)
	source_ip 	= forms.CharField(label='source ip', max_length=50)
	typ 		= forms.ChoiceField(label='type', choices=NAMESYSTEM_TYPES)
	blocks		= forms.CharField(label='Blocks (split based on whitesplace)',widget=forms.Textarea)
	destinations= forms.CharField(label='Destinations (split based on whitespace)', widget=forms.Textarea)
