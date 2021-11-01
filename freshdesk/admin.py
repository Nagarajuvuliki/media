from django.contrib import admin
from .models import FreshDeskTicket, FreshDeskAgent, Converjations
# Register your models here.
class FreshDeskTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'subject', 'priority', 'status', 'created_date']
    
class FreshDeskAgentAdmin(admin.ModelAdmin):
    list_display = ['agent_id', 'email', 'name', 'occasional', 'language', 'created_date']

class ConverjationsAdmin(admin.ModelAdmin):
    list_display = ('from_email', 'user_id', 'body_text', 'to_email', 'ticket_id')
    #list_editable = ('is_active',)
    #list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(FreshDeskTicket, FreshDeskTicketAdmin)
admin.site.register(FreshDeskAgent, FreshDeskAgentAdmin)
admin.site.register(Converjations, ConverjationsAdmin)
