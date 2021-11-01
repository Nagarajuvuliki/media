from django.db import models

# Create your models here.
class AWSEmail(models.Model):
    sender_name = models.EmailField(max_length=100)
    receiver_name = models.EmailField(max_length=100)
    cc_name = models.EmailField(max_length=100, blank=True, null=True)
    bcc_name = models.EmailField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=90)
    body = models.TextField(blank=True, null=True)
    #document = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    #body_html_p = models.CharField(max_length=90, blank=True, null=True)
    #document = models.FileField(upload_to='documents/', blank=True, null=True) 
    
    def __str__(self):
        return self.subject
    
class AWSEmailFiles(models.Model):
    email_id = models.IntegerField(blank=True, null=True)
    receiver_name = models.EmailField(max_length=100, default=None)
    document = models.FileField(upload_to='aws_email_files/', blank=True, null=True) 
    
    def __str__(self):
        return self.receiver_name