from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
	
	log_id = models.AutoField(primary_key=True)
	log_timestamp = models.DateTimeField()
	log_type = models.CharField(max_length=20)
	source_ip = models.CharField(max_length=50)

class Access_Arguments(models.Model):
	
	access_arguments_log	 		= models.OneToOneField(
		
		Log,
		on_delete=models.CASCADE,
		primary_key=True
	)

	access_arguments_user_id 		= models.CharField(max_length=50)
	access_arguments_http_method 	= models.CharField(max_length=20)
	access_arguments_resource 		= models.TextField()
	access_arguments_response 		= models.IntegerField()
	access_arguments_size 			= models.IntegerField()
	access_arguments_referer		= models.TextField()
	access_arguments_agent_string	= models.TextField()

class Dataxceiver_Arguments(models.Model):
	
	dataxceiver_arguments_log		= models.OneToOneField(
		Log,
		on_delete=models.CASCADE,
		primary_key=True
	)

	dataxceiver_arguments_block_id	= models.CharField(max_length=50)
	dataxceiver_arguments_dest_ip	= models.CharField(max_length=50)
	dataxceiver_arguments_size 		= models.IntegerField(null=True)

class Namesystem_Blocks(models.Model):
	
	namesystem_blocks_id 			= models.AutoField(primary_key=True)
	namesystem_blocks_log	 		= models.ForeignKey(Log, on_delete=models.CASCADE)
	namesystem_blocks_block_id 		= models.CharField(max_length=50)

class Namesystem_Destinations(models.Model):
	
	namesystem_destinations_id		= models.AutoField(primary_key=True)
	namesystem_destinations_log		= models.ForeignKey(Log, on_delete=models.CASCADE)
	namesystem_destinations_dest_ip	= models.CharField(max_length=50)

class User_Address(models.Model):
	user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	address = models.CharField(max_length=200)

class User_History(models.Model):
	user_history_id 		= models.AutoField(primary_key=True)
	user_history_username	= models.CharField(max_length=100)
	user_history_action 	= models.TextField()
	user_history_timestamp	= models.DateTimeField(auto_now_add=True)