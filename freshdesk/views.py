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
from .models import FreshDeskTicket, FreshDeskAgent, Converjations
from .serializers import FreshDeskTicketSerializers, FreshDeskAgentSerializers
from rest_framework.decorators import api_view
import os
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
domain = 'kslegal'
api_key = 'n6yB2JxKJBPddPair'
password = 'Themedius789'
headers = { 'Content-Type' : 'application/json' }
# Create your views here.

#webhook
class webhook(ListAPIView):
    
    def get(self, request):
        print('hi')
        logging.basicConfig(filename = 'test.log', level = logging.DEBUG)
        data = self.request.data
        data = str(data)
        print(data)
        print(self.request)
        logging.debug(data)
        return HttpResponse(data)
    
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

def deleteAgent(request, id):
    
    if request.method == 'DELETE':
        agent_id = str(id)
        r = requests.delete("https://{0}.freshdesk.com/api/v2/agents/{1}".format(domain, agent_id), auth = (api_key, password))

        if r.status_code == 204:
            print ("Agent deleted successfully")
            try:
                obj = FreshDeskAgent.objects.get(agent_id=int(agent_id))
                obj.delete()
                return Response({'status': True},status=status.HTTP_200_OK)
                
            except:
                err_res = {
                    'status': False,
                    'message': 'Fields name are not vailid',
                    'data': None
                }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
        else:
            err_res = {
                    'status': False,
                    'message': 'Agent not deleted',
                    'data': None
                }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)

class CreateAgent(ListAPIView):
    
    def post(self, request):
        agents = self.request.data
        r = requests.post("https://{0}.freshdesk.com/api/v2/agents".format(domain), auth = (api_key, password), headers = headers, data = json.dumps(agents))

        if r.status_code == 201:
            print ("Agent created successfully, the response is given below")
        else:
            print ("Failed to create agent, errors are displayed below")
        response = json.loads(r.content.decode('utf-8'))

        t = r.json()
        print(r.json())
        try:
            #print(t["id"])
            FreshDeskAgent.create(agent_id = t["id"], email = agents["email"], name = agents["name"], ticket_scope = int(agents["ticket_scope"]),occasional = agents["occasional"], language = agents["language"])
            return Response({'status': True,'data':r.json()},status=status.HTTP_200_OK)
        except:
            err_res = {
                    'status': False,
                    'message': 'database naming error',
                    'data': None
                }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def UpdateTicket(request, id):    
    #def put(self, request, id):
    if request.method == 'PUT':
        ticket_id = str(id)
        ticket = request.data
        print('hetre')
        # return JsonResponse("")
        
        r = requests.put("https://{0}.freshdesk.com/api/v2/tickets/{1}".format(domain, ticket_id), auth = (api_key, password), headers = headers, data = json.dumps(ticket))
        response = json.loads(r.content.decode('utf-8'))
        if r.status_code == 200:
            print ("Ticket updated successfully, the response is given below")
        else:
            print ("Failed to update ticket, errors are displayed below")
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)

        #response = json.loads(r.content.decode('utf-8'))

        t = r.json()
        try:
            obj = FreshDeskTicket.objects.get(ticket_id=int(id))
        except:
            err_res = {
                        'status': False,
                        'message': 'database naming error',
                        'data': None
                    }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
        serializer = FreshDeskTicketSerializers(instance = obj, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_200_OK)
   
@api_view(['GET'])
def filterTicket(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        print(query)
        r = requests.get("https://" + domain + ".freshdesk.com/api/v2/search/tickets?query="+query, auth = (api_key, password))
        if r.status_code == 200:
            #print ("Ticket deleted successfully")
            print ("Request processed successfully, the response is given below")
            res = {
                "success": True,
                "message": "Ticket Updated",
                
            }
            tickets = r.json()
            #return JsonResponse(res)
            return Response({'status': True,'data':r.json()},status=status.HTTP_200_OK)
        else:
            print ("Failed to delete ticket, errors are displayed below")
            #return JsonResponse(r.json())
            err_res = {
                    'status': False,
                    'message': 'database naming error',
                    'data': None
                }
            return Response({'data':r.json()}, status=status.HTTP_400_BAD_REQUEST)
        #response = json.loads(r.content.decode('utf-8'))

        

        
def deleteTikcet(request, id):
    if request.method == 'DELETE':
        ticket_id = id
        r = requests.delete("https://{0}.freshdesk.com/api/v2/tickets/{1}".format(domain, ticket_id), auth = (api_key, password))

        if r.status_code == 204:
            print ("Ticket deleted successfully")
            try:
                obj = FreshDeskTicket.objects.get(ticket_id=ticket_id)
                obj.delete()
                return Response({'status': True},status=status.HTTP_200_OK)
            except:
                err_res = {
                    'status': False,
                    'message': 'database naming error',
                    'data': None
                }
                return Response(err_res, status=status.HTTP_400_BAD_REQUEST)


class DeleteMultipleTikcets(ListAPIView):

    def post(self, request):
        data = self.request.data
        print("received data : ",data)
        
        ticket_ids = data
        #print(ticket_ids["bulk_action"]["ids"],'  bjb')
        #return
        r = requests.post("https://{0}.freshdesk.com/api/v2/tickets/bulk_delete".format(domain),headers = headers, auth = (api_key, password), data = json.dumps(ticket_ids))

        if r.status_code == 202:
            try:
                for i in ticket_ids["bulk_action"]["ids"]:
                    obj = FreshDeskTicket.objects.get(ticket_id=i)
                    obj.delete()
                    return Response({'status': True},status=status.HTTP_200_OK)
            except:
                err_res = {
                    'status': False,
                    'message': 'database naming error',
                    'data': None
                }
                return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
            
#from get_ticket_ids import get_ticket_ids
def save_converjation_in_databse(request):
    
    r = requests.get("https://{0}.freshdesk.com/api/v2/tickets/".format(domain), auth = (api_key, password))

    if r.status_code == 200:
        print ("Request processed successfully, the response is given below")
    else:
        print ("Failed to read ticket, errors are displayed below")
    response = json.loads(r.content.decode('utf-8'))

    tickets = r.json()
    ticket_ids = []
    for i in tickets:
        ticket_ids.append(i["id"])
    for ticket_id in ticket_ids:
        try:
            r = requests.get("https://{0}.freshdesk.com/api/v2/tickets/{1}/conversations".format(domain, ticket_id), auth = (api_key, password))
        except:
            err_res = {
                    'status': False,
                    'message': 'database naming error',
                    'data': None
                }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
        if r.status_code == 200:
            print ("Request processed successfully, the response is given below")
        else:
            print ("Failed to read ticket, errors are displayed below")
        response = json.loads(r.content.decode('utf-8'))

        tickets = r.json()
        #print(json.dumps(tickets))
        
        
        if tickets:
            for i in tickets:
                print('hi')
                if i["support_email"] and i["user_id"] and i["body_text"] and i["to_emails"] and i["ticket_id"]:
                    try:
                        obj = Converjations.objects.get(from_email = i["support_email"], user_id = i["user_id"], body_text = i["body_text"], to_email = i["to_emails"][0], ticket_id = i["ticket_id"])
                    except Converjations.DoesNotExist:
                        Converjations(from_email = i["support_email"], user_id = i["user_id"], body_text = i["body_text"], to_email = i["to_emails"][0], ticket_id = i["ticket_id"]).save()
    return Response({'status': True},status=status.HTTP_200_OK)
    

class CreateTikcet(ListAPIView):
    
    def post(self, request):
        ticket = self.request.data
        webhook_url = 'https://webhook.site/bb50cb98-7f1c-48ff-9850-82d1af4f4da5'
        data = ticket
        r = requests.post(webhook_url, data = json.dumps(data), headers = {"Content-Type": "application/json"})
        r = requests.post("https://{0}.freshdesk.com/api/v2/tickets".format(domain), auth = (api_key, password), headers = headers, data = json.dumps(ticket))

        if r.status_code == 201:
            print ("Ticket created successfully, the response is given below")
        else:
            err_res = {
                    'status': False,
                    'message': 'database naming error',
                    'data': None
                }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
        response = json.loads(r.content.decode('utf-8'))
        
        t = r.json()
        print(r.json())
        if ticket["description"] is None:
            ticket["description"] = ""
        #try:
        FreshDeskTicket.create(ticket_id=int(t["id"]), subject=ticket["subject"], description = ticket["description"], email = ticket["email"], priority=int(ticket["priority"]), status=int(ticket["status"]))
        #except:
            #return JsonResponse(database_error())
        return Response({'status': True, 'data':t},status=status.HTTP_200_OK)
    
@api_view(('GET',))
#@renderer_classes((JSONRenderer, ))
def view_tickets(request):
    r = requests.get("https://{0}.freshdesk.com/api/v2/tickets/".format(domain), auth = (api_key, password))

    if r.status_code == 200:
        print ("Request processed successfully, the response is given below")
    else:
        err_res = {
                    'status': False,
                    'message': 'database naming error',
                    'data': None
                }
        return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
    response = json.loads(r.content.decode('utf-8'))

    tickets = r.json()
    result = {'data': tickets}
    print(result)
    #return HttpResponse(tickets)
    serializer = FreshDeskTicketSerializers(FreshDeskTicket.objects.all(), many = True)
    return Response(serializer.data)