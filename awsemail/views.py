from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from rest_framework.generics import ListAPIView
#from rest_framework.response import Response
#from rest_framework import status
#from . serializers import employeesSerializer
#from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
import ast
import json
from .models import AWSEmail, AWSEmailFiles
import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import logging
import json
import awswrangler as wr
import pandas as pd
import boto3
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def store_file_on_aws(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        for file in files:
            #file = request.POST.get('file')
            print('here')
            print(file)
            df = pd.read_excel(file, nrows = 5)
            print(df)
            df.to_excel(file)
            return HttpResponse('done')
        '''s3 = boto3.resource('s3')
        try:
            BUCKET_NAME = 'themedius.ai'
            object = s3.Object('themedius.ai', str(file))
            uri = f"store_xl/{str(file)}"#enter path to store
            object.put(ACL='public-read', Body=file.read(), Key=uri)
            uri = f"s3://{BUCKET_NAME}/" + uri
            print(uri)
            print('done')
        except Exception as e:
            uri = None
            print('not done')
            pass'''
        

def database_error():
    res = {
        "success" : False,
        #"Error Type" : "Ticket is created but not store in databse",
        "Reason" : """May be you are using wrong names kindly check it these are same as below or not
            Name for subject is: subject
            Name for description is: description
            Name for priority is: priority
            Name for status is: status
            Note: You are using integer values for priority and status"""
    }   
    return res

class SendEmail(ListAPIView):
    
    def post(self, request):
        #process to store email data on aws s3
        email_detail = self.request.data
        SENDER = 'careers@getgologistics.com'#str(request.POST['sender_name'])
        SENDERNAME = 'GetGoLogistics'
        RECIPIENT  = request.POST["RecipientName"]   #email_detail["RecipientName"]
        USERNAME_SMTP = "AKIAWD5APCVRDZFVHPEL"
        PASSWORD_SMTP = "BB22dMY7qfT4cduhAnn+fnkuGWNyLZH46X0PRpWZil+a"
        HOST = "email-smtp.ap-south-1.amazonaws.com"
        PORT = 587
        SUBJECT = request.POST.get("Subject")  #email_detail["Subject"]
        BODY_TEXT = ""
        BODY_HTML = request.POST.get("Body") #email_detail["Body"]
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
        msg['To'] = RECIPIENT
        isCc = isBcc = True
        cc = bcc = ""

        if request.POST.get('Cc'): #email_detail["Cc"]:
            msg['Cc'] = request.POST.get('Cc') #email_detail["Cc"]
            cc = request.POST.get('Cc')
        if request.POST.get('Bcc'): #email_detail["Bcc"]:
            msg['Bcc'] = request.POST.get('Bcc') #email_detail["Bcc"]
            bcc = request.POST.get('Bcc')
        part1 = MIMEText(BODY_TEXT, 'plain')
        part2 = MIMEText(BODY_HTML, 'html')
        msg.attach(part1)
        msg.attach(part2)
        if request.FILES:
            files = request.FILES.getlist('document')
            
            for file in files:
                print(file)
                print(type(file))
                s3 = boto3.resource('s3')
                try:
                    BUCKET_NAME = 'themedius.ai'
                    object = s3.Object('themedius.ai', str(file))
                    uri = f"AWS_Email/send_email_files/{str(file)}"#enter path to store
                    object.put(ACL='public-read', Body=file.read(), Key=uri)
                    uri = f"s3://{BUCKET_NAME}/" + uri
                    print(uri)
                    print('done')
                except Exception as e:
                    uri = None
                    print('not done')
                    pass

                obj = AWSEmailFiles(receiver_name = RECIPIENT, document = file)
                obj.save()
                path = os.getcwd()
                path = path.replace('\\', '/')
                #return HttpResponse(path)
                path += '/media/aws_email_files/'
                path += str(file)#str(fm.cleaned_data['document'].name)
                print(path)
                ATTACHMENT = path
                att = MIMEApplication(open(ATTACHMENT, 'rb').read())
                att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))
                msg.attach(att)
        # Try to send the message.
         
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        #server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()

        try:
            obj = AWSEmail(sender_name = SENDER, receiver_name = RECIPIENT, cc_name = cc, bcc_name = bcc, subject = SUBJECT, body = BODY_HTML)
            obj.save()
        except:
            err_res = {
                    'status': False,
                    'message': 'fail to save in database',
                    'data': None
                }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': True, 'message': 'email sent'},status=status.HTTP_200_OK)
        # Display an error message if something goes wrong.
