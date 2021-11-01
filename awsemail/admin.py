from django.contrib import admin
from .models import AWSEmail
# Register your models here.
class AWSEmailAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'receiver_name', 'subject', 'body', 'created_date']
    

admin.site.register(AWSEmail, AWSEmailAdmin)
