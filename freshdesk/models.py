from django.db import models

# Create your models here.

class FreshDeskTicket(models.Model):
    ticket_id = models.IntegerField()
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True, null = True)
    email = models.EmailField(max_length=100, default="")
    priority = models.IntegerField()
    status = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject
    
    @classmethod
    def create(cls, ticket_id, subject, description, email, priority, status):
        data = cls(ticket_id=ticket_id, subject=subject, description=description, priority=priority, status=status)
        # do something with the book
        data.save()
        return
    
class FreshDeskAgent(models.Model):
    agent_id = models.BigIntegerField()
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    ticket_scope = models.IntegerField() 
    occasional = models.BooleanField(default=None) 
    language = models.CharField(max_length=100, default="")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def create(cls, agent_id, email, name, ticket_scope, occasional, language):
        data = cls(agent_id = agent_id, email = email, name = name, ticket_scope = ticket_scope,occasional = occasional, language = language)
        # do something with the book
        data.save()
        return
    
class Converjations(models.Model):
    from_email = models.CharField(max_length=100)# is:  popatnirmal2233@gmail.com
    user_id = models.CharField(max_length=100)# is:  82029555042
    body_text = models.TextField()# is : Hello FreshDesk
    to_email = models.CharField(max_length=100)# is : "NP Online service limited" <support@newaccount1628324519111.freshdesk.com>
    ticket_id = models.IntegerField()# is : 18    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    @classmethod
    def create(cls, from_email = from_email, user_id = user_id, body_text = body_text, to_email = to_email, ticket_id = ticket_id):
        data = cls(from_email = from_email, user_id = user_id, body_text = body_text, to_email = to_email, ticket_id = ticket_id)
        # do something with the book
        data.save()
        return