from django.contrib import admin

from .models import User_Address, Log, Access_Arguments, Dataxceiver_Arguments, Namesystem_Blocks, Namesystem_Destinations

admin.site.register(User_Address)
admin.site.register(Log)
admin.site.register(Access_Arguments)
admin.site.register(Dataxceiver_Arguments)
admin.site.register(Namesystem_Blocks)
admin.site.register(Namesystem_Destinations)