from django.contrib import admin
from .models import *


class ChatUserAdmin(admin.ModelAdmin):
    list_display=('id','phone','email','username','full_name','gender','country')
admin.site.register(ChatUser,ChatUserAdmin)


class InterestAdmin(admin.ModelAdmin):
    list_display=('id','name')
admin.site.register(Interest,InterestAdmin)

class ConnectionAdmin(admin.ModelAdmin):
    list_display=('id','user1','user2')
admin.site.register(Connection,ConnectionAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display=('id','content','sender','connection')
admin.site.register(Message,MessageAdmin)
