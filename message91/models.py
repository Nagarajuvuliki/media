from django.db import models

# Create your models here.
class Message(models.Model):
    message_language = models.CharField(max_length=100)
    message_body = models.TextField()
    message_instance = models.CharField(max_length=100)
    #state = models.CharField(max_length=100)
    template_id = models.CharField(max_length=100, default = None, blank = True, null = True)
    flow_id = models.CharField(max_length=200, default = None, blank = True, null = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.message_body
    
class Contact(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    message_body = models.TextField()
    message_instance = models.CharField(max_length=100, default = None)
    batch_id = models.IntegerField(default=1)
    is_message_sent = models.BooleanField(default=True)
    
    def __str__(self):
        return self.customer_name
    
class SaveBatchConversation(models.Model):
    #customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100, default = None)
    #message_body = models.TextField(default=None)
    #message_instance = models.CharField(max_length=100, default=None)
    batch_id = models.IntegerField(default = None)
    created_date = models.DateTimeField(auto_now_add=True)
   # #is_message_sent = models.BooleanField(default=True)

class MessageConversation(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    #product_name = models.CharField(max_length=100, default = None)
    message_body = models.TextField(default=None)
    #message_instance = models.CharField(max_length=100, default=None)
    batch_id = models.IntegerField(default = None)
    is_message_sent = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
