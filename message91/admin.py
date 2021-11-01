from django.contrib import admin
from .models import  Contact, SaveBatchConversation, MessageConversation, Message
# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','message_language', 'message_body', 'message_instance', 'flow_id', 'created_date')
    
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','customer_name', 'contact_number', 'state','message_body', 'message_instance', 'is_message_sent')

class SaveBatchConversationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'contact_number', 'state','product_name','batch_id')
    
class MessageConversationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'contact_number', 'state','message_body','batch_id', 'is_message_sent')
    
admin.site.register(Message, MessageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(SaveBatchConversation, SaveBatchConversationAdmin)
admin.site.register(MessageConversation, MessageConversationAdmin)
