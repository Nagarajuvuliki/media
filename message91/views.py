from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Contact, Message, SaveBatchConversation, MessageConversation
import awswrangler as wr
import pandas as pd
import boto3
import json
import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import http.client
from .serializers import MessageSerializers
import http.client
# Create your views here.
#STATE WISE RULES Dictonry
state_wise_rulses = {
    "maharashtra": {
        "PRIMARY_LANG": "Pure Marathi",
        "SECONDARY_LANG": "Hindi-Eng",
    },
    "assam": {
        "PRIMARY_LANG": "Pure Bengali",
        "SECONDARY_LANG": "Hindi-Eng",
    },
    "bengal": {
        "PRIMARY_LANG": "Pure Bengali",
        "SECONDARY_LANG": "Hindi-Eng",
    },
    "tamilnadu": {
        "PRIMARY_LANG": "Pure-Tamil",
        "SECONDARY_LANG": "Pure English",
    },
    "karnataka": {
        "PRIMARY_LANG": "Pure Kannada",
        "SECONDARY_LANG": "Pure English",
    },
    "telangana": {
        "PRIMARY_LANG": "Pure Telugu",
        "SECONDARY_LANG": "Pure English",
    },
    "kerela": {
        "PRIMARY_LANG": "Pure Malyalam",
        "SECONDARY_LANG": "Pure English",
    },
    "all_other_state": {
        "PRIMARY_LANG": "Hindi-Eng",
        "SECONDARY_LANG": "Pure English",
    },
}

@api_view(['POST'])
def add(request):
    if request.method == 'POST':
        try:
            if request.POST.get('message_language') and request.POST.get('message_body') and request.POST.get('message_instance'):
                Message(message_language = request.POST.get('message_language'), message_body = request.POST.get('message_body'), message_instance = request.POST.get('message_instance')).save()
            return Response({'status': True},status=status.HTTP_201_CREATED)
        except:
            #return HttpResponse('Database Error')
            err_res = {
                    'status': False,
                    'message': 'Fields name are not vailid',
                    'data': None
                }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def update(request, id):
    if request.method == 'POST':
        try:
            obj = Message.objects.get(id = id)
        except:
            err_res = {
                    'status': False,
                    'message': 'Fields name are not vailid',
                    'data': None
                }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
        serializer = MessageSerializers(instance = obj, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        if request.POST.get('message_language'):
            obj.message_language = request.POST.get('message_language')
        if request.POST.get('message_body'):
            obj.message_body = request.POST.get('message_body')
        if request.POST.get('message_instance'):
            obj.message_instance = request.POST.get('message_instance')
        obj.save()
        return Response({'status': True},status=status.HTTP_200_OK)
        
@api_view(['POST'])
def delete(request, id):
    if request.method == 'POST':
        try:
            Message.objects.get(id = id).delete()
            return Response({'status': True},status=status.HTTP_200_OK)
        except:
            err_res = {
                    'status': False,
                    'message': 'Fields name are not vailid',
                    'data': None
                }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)

def get_customer_data():
    client = boto3.client('athena')


    queryStart = client.start_query_execution(
        QueryString = "select * from message91_customer_deteails",
        QueryExecutionContext = {
            'Database': 'the_medius_database'
        }, 
        ResultConfiguration = { 'OutputLocation': 's3://themedius.ai/Batch_Database/'}
    )

    queryExecutionId = queryStart.get('QueryExecutionId')

    while True:
        query_state = client.get_query_execution(QueryExecutionId=queryExecutionId).get('QueryExecution').get('Status').get('State')
        if query_state == 'SUCCEEDED' or query_state == 'FAILED' or query_state == 'CANCELLED':
            print(query_state)
            print('breakkkinggg...')
            break

    if query_state == 'SUCCEEDED':
        results = client.get_query_results(QueryExecutionId=queryExecutionId)
        
    column_mapper = {}
    final_results = []

    for row in range(len(results['ResultSet']['Rows'])):
        fields = results['ResultSet']['Rows'][row]
        

        if row == 0:
            for i in range(len(fields['Data'])):
                if bool(fields['Data'][i]):
                    column_mapper.update({i: list(fields['Data'][i].values())[0]})
        else:
            temp = {}
            for i in range(len(fields['Data'])):
                if bool(fields['Data'][i]):
                    temp.update({column_mapper.get(i): list(fields['Data'][i].values())[0]})
                else:
                    temp.update({column_mapper.get(i): 'None'})
            final_results.append(temp)
    return final_results

@api_view(['POST'])
def send_message(request, batch_id):
    #customer_data = get_customer_data()
    #print(customer_data)
    customer_data = SaveBatchConversation.objects.filter(batch_id=batch_id)
    #process to store sent messages in s3
    product_cat = {
        'Personal Loan': 'Property',
        'Bike': 'Bike',
        'Car': 'Car',
        'Tractor': 'Tractor'
    }
    if request.method == 'POST':
        for customer in customer_data:
            state = customer.state
            check = False
            for i in state_wise_rulses:
                if i == state:
                    check = True
            if check:
                state = state
            else:
                state = 'all_other_state'
            message_state = state_wise_rulses[state]
            instance = 'When batch is uploaded'
            #print(request.POST.get('message_instance'))
            #print(request.POST.get('message_instance') == 'When batch is uploaded')
            if instance == 'When batch is uploaded':
                print('herreeeee')
                message_content1 = message_state["PRIMARY_LANG"]
                message_content2 = message_state["SECONDARY_LANG"]
                first_message = '<cust_first_name>, <product_cat_1>ka TVS EMI baaki hai.Pay karne ke liye abhi<helpline_var>par call kariye.Warna <product_cat_2> japt ki jayegi.'
                second_message = '<cust_first_name>, <product_cat_1>ka TVS EMI baaki hai.Pay karne ke liye abhi<helpline_var>par call kariye.Warna <product_cat_2> japt ki jayegi.'
                print(first_message, second_message)
                first_message = str(first_message)
                second_message = str(second_message)
                try:
                    first_message = first_message.replace('<cust_first_name>', customer.customer_name)
                    try:
                        first_message = first_message.replace('<product_cat_1>', customer.product_name)
                    except:
                        pass
                    try:
                        first_message = first_message.replace('<product_cat_2>', customer.product_name)
                    except:
                        pass
                    try:
                        first_message = first_message.replace('<helpline_num>', '1800 1800 1800')
                    except:
                        pass
                    try:
                        first_message = first_message.replace('<helpline_var>', '1800 1800 1800')
                    except:
                        pass
                    
                
                    second_message = second_message.replace('<cust_first_name>', customer.customer_name)
                    try:
                        second_message = second_message.replace('<product_cat_1>', customer.product_name)
                    except:
                        pass
                    try:
                        second_message = second_message.replace('<product_cat_2>', customer.product_name)
                    except:
                        pass
                    try:
                        second_message = second_message.replace('<helpline_num>', '1800 1800 1800')
                    except:
                        pass
                    try:
                        second_message = second_message.replace('<helpline_var>', '1800 1800 1800')
                    except:
                        pass
                except:
                    pass
                try:
                    obj = MessageConversation.objects.get(customer_name = customer.customer_name, contact_number = customer.contact_number, state = customer.state, message_body = first_message, batch_id = int(customer.batch_id), is_message_sent = True).save()
                except MessageConversation.DoesNotExist:
                    MessageConversation(customer_name = customer.customer_name, contact_number = customer.contact_number, state = customer.state, message_body = first_message, batch_id = int(customer.batch_id), is_message_sent = True).save()

                try:
                    obj = MessageConversation.objects.get(customer_name = customer.customer_name, contact_number = customer.contact_number, state = customer.state, message_body = second_message, batch_id = int(customer.batch_id), is_message_sent = True).save()
                except MessageConversation.DoesNotExist:
                    MessageConversation(customer_name = customer.customer_name, contact_number = customer.contact_number, state = customer.state, message_body = second_message, batch_id = int(customer.batch_id), is_message_sent = True).save()
                if customer.product_name == 'Personal Loan':
                    product1 = 'Personal Loan'
                    product2 = 'Property'
                else:
                    product1 = product2 = customer.product_name
                conn = http.client.HTTPSConnection("api.msg91.com")
                
                payload = {
                                "flow_id": "61351c0cb37c5a19e3550de2",
                                "sender": "KSLEGL",
                                "mobiles": customer.contact_number,
                                "var1": customer.customer_name,
                                "var2": product1,
                                "var3": "1800-1800-1800",
                                "var4": product2
                    }#.format(customer.contact_number, customer.customer_name, product1, product2)
                payload = json.dumps(payload)
                print(payload)
                headers = {
                                'authkey': "365647AwrThz5RTww6113a1fcP1",
                                'content-type': "application/JSON"
                          }
                
                conn.request("POST", "/api/v5/flow/", payload, headers)

                res = conn.getresponse()
                data = res.read()
                print(data.decode("utf-8"))
                
                #process to stire sent messages in aws s3
                '''data = {
                    'customer_id':[customer['c_id'], customer['c_id']],
                    'customer_name':[customer['name'], customer['name']],
                    'contact_number':[customer['phone_number'], customer['phone_number']],
                    'state':[customer['state'], customer['state']],
                    'message_body':[first_message, second_message],
                    'message_instance':[instance, instance],
                    'batch_id':[customer['batch_id'], customer['batch_id']],
                    'is_message_sent':['yes','yes']
                }
                
                df = pd.DataFrame(data)

                DTYPES = {
                        'customer_id':'int',
                        'customer_name': 'string',
                        'contact_number': 'string',
                        'state': 'string',
                        'message_body': 'string',
                        'message_instance': 'string',
                        'batch_id': 'int',
                        'is_message_sent':'string'
                }
                database = 'the_medius_database'
                BUCKET_NAME = 'themedius.ai'
                db_table_name = 'message_converjations'
                description = 'this is my test table for sent message'

                write_path = f"s3://{BUCKET_NAME}/Message91/"
                
                reponse = wr.s3.to_parquet(df=df, path=write_path, dataset=True, mode='append', database=database, table=db_table_name, dtype=DTYPES, description=description)
                uri_path = None
                if len(reponse.get('paths')) > 0:
                    uri_path = reponse.get('paths')[0]
                print(uri_path)'''
                                        
                #Contact(customer_name = request.POST.get('customer_name'), contact_number = request.POST.get('contact_number'), state = request.POST.get('state'), message_body = first_message, message_instance = request.POST.get('message_instance')).save()
                #Contact(customer_name = request.POST.get('customer_name'), contact_number = request.POST.get('contact_number'), state = request.POST.get('state'), message_body = second_message, message_instance = request.POST.get('message_instance')).save()
            else:
                
                message_content2 = message_state["SECONDARY_LANG"]
                #print(message_content2, request.POST.get('message_instance'))
                print(message_content2)
                print(instance)
                second_message = Message.objects.get(message_language = message_content2, message_instance = instance)
                second_message = str(second_message)
                try:
                    second_message = second_message.replace('<cust_first_name>', customer.customer_name)
                    try:
                        second_message = second_message.replace('<product_cat_1>', customer.product_name)
                    except:
                        pass
                    try:
                        second_message = second_message.replace('<product_cat_2>', customer.product_name)
                    except:
                        pass
                    try:
                        second_message = second_message.replace('<helpline_num>', '1800 1800 1800')
                    except:
                        pass
                    try:
                        second_message = second_message.replace('<helpline_var>', '1800 1800 1800')
                    except:
                        pass
                except:
                    pass
                try:
                    obj = MessageConversation.objects.get(customer_name = customer.customer_name, contact_number = customer.contact_number, state = customer.state, message_body = second_message, batch_id = int(customer.batch_id), is_message_sent = True).save()
                except MessageConversation.DoesNotExist:
                    MessageConversation(customer_name = customer.customer_name, contact_number = customer.contact_number, state = customer.state, message_body = second_message, batch_id = int(customer.batch_id), is_message_sent = True).save()

                '''data = {
                    'customer_id':[customer['c_id']],
                    'customer_name':[customer['name']],
                    'contact_number':[customer['phone_number']],
                    'state':[customer['state']],
                    'message_body':[second_message],
                    'message_instance':[instance],
                    'batch_id':[customer['batch_id']],
                    'is_message_sent':['yes']
                }
                
                df = pd.DataFrame(data)

                DTYPES = {
                        'customer_id':'int',
                        'customer_name': 'string',
                        'contact_number': 'string',
                        'state': 'string',
                        'message_body': 'string',
                        'message_instance': 'string',
                        'batch_id': 'int',
                        'is_message_sent':'string'
                }
                database = 'the_medius_database'
                BUCKET_NAME = 'themedius.ai'
                db_table_name = 'message_converjations'
                description = 'this is my test table for sent message'

                write_path = f"s3://{BUCKET_NAME}/Message91/"
                
                reponse = wr.s3.to_parquet(df=df, path=write_path, dataset=True, mode='append', database=database, table=db_table_name, dtype=DTYPES, description=description)
                uri_path = None
                if len(reponse.get('paths')) > 0:
                    uri_path = reponse.get('paths')[0]
                print(uri_path)'''
        
                        #Contact(customer_name = request.POST.get('customer_name'), contact_number = request.POST.get('contact_number'), state = request.POST.get('state'), message_body = second_message, message_instance = request.POST.get('message_instance')).save()
                #return HttpResponse('Added')
            '''except:
     
               return HttpResponse('Database Error')'''
        return Response({'status': True},status=status.HTTP_200_OK)

def get_message_converjations_data():
    client = boto3.client('athena')


    queryStart = client.start_query_execution(
        QueryString = "select * from batch_table",
        QueryExecutionContext = {
            'Database': 'the_medius_database'
        }, 
        ResultConfiguration = { 'OutputLocation': 's3://themedius.ai/Batch_Database/'}
    )

    queryExecutionId = queryStart.get('QueryExecutionId')

    while True:
        query_state = client.get_query_execution(QueryExecutionId=queryExecutionId).get('QueryExecution').get('Status').get('State')
        if query_state == 'SUCCEEDED' or query_state == 'FAILED' or query_state == 'CANCELLED':
            print(query_state)
            print('breakkkinggg...')
            break

    if query_state == 'SUCCEEDED':
        results = client.get_query_results(QueryExecutionId=queryExecutionId)
        
    column_mapper = {}
    final_results = []

    for row in range(len(results['ResultSet']['Rows'])):
        fields = results['ResultSet']['Rows'][row]
        

        if row == 0:
            for i in range(len(fields['Data'])):
                if bool(fields['Data'][i]):
                    column_mapper.update({i: list(fields['Data'][i].values())[0]})
        else:
            temp = {}
            for i in range(len(fields['Data'])):
                if bool(fields['Data'][i]):
                    temp.update({column_mapper.get(i): list(fields['Data'][i].values())[0]})
                else:
                    temp.update({column_mapper.get(i): 'None'})
            final_results.append(temp)
    return final_results

@api_view(('GET',))
def get_message_converjations(request):
    customer_data = MessageConversation.objects.all()
    c = 0
    data = []
    for customer in customer_data:
        temp = {}
        temp['customer_name'] = customer.customer_name
        temp['contact_number'] = customer.contact_number
        temp['state'] = customer.state
        temp['message_body'] = customer.message_body
        #temp['message_instance'] = customer.message_instance
        temp['batch_id'] = customer.batch_id
        temp['is_message_sent'] = customer.is_message_sent
        data.append(temp)
    result = {'data': data}
    return Response({'status': True, 'data': result},status=status.HTTP_200_OK)

@api_view(('GET',))
@renderer_classes((JSONRenderer, ))
def get_message_converjations_by_batch_id(request, batch_id):
    customer_data = get_message_converjations_data()
    print(customer_data)
    #return HttpResponse('hi')
    c = 0
    data = []
    for customer in customer_data:
        if int(customer['batch_id']) == batch_id:
            print(customer)
            try:
                state = customer['state']
            except:
                state = 'all_other_state'
            
            try:
                obj = SaveBatchConversation.objects.get(customer_name=customer['customer_name'],contact_number=customer['customer_mobile_number'],state=state,product_name=customer['product_name'],batch_id=int(customer['batch_id']))
            except SaveBatchConversation.DoesNotExist:
                obj = SaveBatchConversation(customer_name=customer['customer_name'],contact_number=customer['customer_mobile_number'],state=state,product_name=customer['product_name'],batch_id=int(customer['batch_id']))
                obj.save()
            #print(customer['customer_id'], 'customer id.....')
            #print(customer.customer_id, 'customer id')
            temp = {}
            #temp['customer_id'] = customer['customer_id']
            temp['customer_name'] = customer['customer_name']
            temp['contact_number'] = customer['customer_mobile_number']
            temp['state'] = state
            temp['product_name'] = customer['product_name']
            temp['batch_id'] = customer['batch_id']
            data.append(temp)
    result = {'status': True, 'data': data}
    #return HttpResponse('done')        
    return Response(result, status=status.HTTP_200_OK)

@api_view(('GET',))
def get_message_converjations_by_customer_mobile_number(request, customer_mobile_number):
    data = []
        #print(SaveBatchConversation.objects.get(customer_id = customer_id))
    customer_data = MessageConversation.objects.filter(contact_number = customer_mobile_number)
    if customer_data:
        for customer in customer_data:
            temp = {}
            temp['customer_name'] = customer.customer_name
            temp['contact_number'] = customer.contact_number
            temp['state'] = customer.state
            temp['message_body'] = customer.message_body
            #temp['message_instance'] = customer.message_instance
            temp['batch_id'] = customer.batch_id
            temp['is_message_sent'] = customer.is_message_sent
            data.append(temp)
        result = {'data': data}
        
        return Response({'status': True, 'data': result},status=status.HTTP_200_OK)
    else:
        err_res = {
                    'status': False,
                    'message': 'Data is not avalable with this given cutomer id',
                    'data': None
                }
        return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
    '''customer_data = get_message_converjations_data()
    c = 0
    data = []
    for i in customer_data:
        if i['customer_id'] == str(customer_id):
            return JsonResponse(i)
    return JsonResponse({})'''
