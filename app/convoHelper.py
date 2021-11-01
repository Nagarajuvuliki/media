from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render
import awswrangler as wr
import pandas as pd
import boto3
import json
import datetime

from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConversationWatiSerializer,Conversation_WatiSerializer
from app.convoAHelper import DTYPES , BATCH_TABLE_HELPER
from .models import ConversationWati,Conversation_Wati

def get_write_path(table_name):
    dir_name = ""
    if table_name in ["ConversationWati"]:
        dir_name = table_name
    return f"s3://themedius.ai/Batch_Database/{table_name}/"




class save_conversations_apii(APIView):

    # def get(self,request,format=None):


        # for c in contact_numbers:

        #     url = "https://live-server-2553.wati.io/api/v1/getMessages/{0}".format(c)

        #     headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0MzE5NjQxMC1iNDA2LTQ0ZDktOWFiYy1lZTE5ZmZiZWMzNWEiLCJ1bmlxdWVfbmFtZSI6IlNvbmFtQGtzbGVnYWwuY28uaW4iLCJuYW1laWQiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiZW1haWwiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiYXV0aF90aW1lIjoiMDgvMDMvMjAyMSAwNToyOToxNCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFETUlOSVNUUkFUT1IiLCJleHAiOjI1MzQwMjMwMDgwMCwiaXNzIjoiQ2xhcmVfQUkiLCJhdWQiOiJDbGFyZV9BSSJ9.d8Z083VdTnmkv4k86NTY6oU6PhRhEi_ldUc-7cHN9Sg"}

        #     response = requests.request("GET", url, headers=headers)

        #     r = response.json()

        #     if response.status_code == 200 and r["result"]=="success":

                

        #         raw_df = pd.json_normalize(r["messages"],record_path=["items"])

        #         raw_df["number"] = c

        #         print(raw_df)

        #         current_date = datetime.date.today().strftime("%Y-%m-%d")

        #         final_dataframes_data = {}

        #         for table in BATCH_TABLE_HELPER:
        #             print('TABLE_NAME>>>', table)
        #             not_found_fields = []
        #             found_fields_data = {}

                    

        #             for field in BATCH_TABLE_HELPER.get(table):

        #                 if field in raw_df.columns:
                            
        #                     found_fields_data.update({field: raw_df[field]})
                            
        #                 else:
        #                     not_found_fields.append(field) 

        #             # print(found_fields_data)
        #             # print(not_found_fields)
                    
        #             temp_df = pd.DataFrame(data=found_fields_data)
        #             temp_df['created_at'] = current_date
                    
        #             for field in not_found_fields:
        #                 temp_df[field] = 'None'
        #         #     print(temp_df.head())

                    

                    
                        
        #             final_dataframes_data.update({
        #                 table: {
        #                     "db_table_name": f"{table}_table",
        #                     "write_path": get_write_path(table),
        #                     "df": temp_df,
        #                     "description": f"this is our {table} database table.",
        #                     "dtype": DTYPES.get(table)
        #                 }
        #             })
                    
                    
        #         final_batch_meta_data = {
        #         'batch_name': 'batch_name'
        #         }

        #         database = 'the_medius_database'

        #         # temp2 = 'wAid'
        #         # for key,val in data["contact_list"]:
        #         #     if temp2 in val:
        #         #         reso = [val[temp2]]
             

        #         for df in final_dataframes_data:
                    
                    
                    
                    
        #             reponse = wr.s3.to_parquet(df=final_dataframes_data.get(df).get('df'), path=final_dataframes_data.get(df).get('write_path'), dataset=True, mode='append', database=database, table=final_dataframes_data.get(df).get('db_table_name'), dtype=final_dataframes_data.get(df).get('dtype'), description=final_dataframes_data.get(df).get('description'))
        #             uri_path = None
        #             if len(reponse.get('paths')) > 0:
        #                 uri_path = reponse.get('paths')[0]
        #             final_batch_meta_data.update({f"{df}_s3_uri": uri_path})

                
        #             # print(final_batch_meta_data)
                    
        #             ConversationWati.objects.create(Conversation_Wati_s3_uri = final_batch_meta_data)


        # get_contact_serializer = ConversationWatiSerializer(data=final_batch_meta_data)
        #         # print(contact_serializer)
        # if get_contact_serializer.is_valid():
        #     batch_obj = get_contact_serializer.save()
                    
        # else:
        #     err_res = {
        #                     'status': False,
        #                     'message': get_contact_serializer.errors,
        #                     'data': None
        #                 }
        #     return Response(err_res, status=status.HTTP_200_OK)
                            
        # response = {
        #                 'status': True,
        #                 'message': 'Conversation data saved sucessfully.',
        #                 # 'data': r["contact_list"]
        #             }
        # return Response(response, status=status.HTTP_201_CREATED)








        
                # number_entered_by_user = request.query_params.get('number')
                # if number_entered_by_user:
                #     queryset = Conversation_Wati.objects.filter(number=number_entered_by_user).order_by('-created')
                # else:
                #     # queryset = Conversation.objects.all().order_by('-sent')
                #     queryset = Conversation_Wati.objects.all().order_by('-created')
                # serializer = Conversation_WatiSerializer(queryset,many = True)
                # # filterset_fields = ['number','name','status']

                # response = {
                #         'status': True,
                #         'message': 'Data fetched successfully.',
                #         'data': serializer.data
                # }
                # return Response(response, status=status.HTTP_200_OK)

        

        def get(self, request, format=None):

            batch_id = self.request.query_params.get('batch_id')

            if batch_id:
        
                S3_BUCKET = 'themedius.ai'

                client = boto3.client('athena')
                queryStart = client.start_query_execution(
                    QueryString = f"SELECT * FROM whatsapp_users_table  where batch_id='{batch_id}'",
                    QueryExecutionContext = {
                        'Database': 'the_medius_database'
                    }, 
                    ResultConfiguration = { 'OutputLocation': 's3://themedius.ai/Batch_Database/'}
                )
                queryExecutionId = queryStart.get('QueryExecutionId')

                while True:
                    query_state = client.get_query_execution(QueryExecutionId=queryExecutionId).get('QueryExecution').get('Status').get('State')
                    print(query_state)
                    if query_state == 'SUCCEEDED' or query_state == 'FAILED' or query_state == 'CANCELLED':
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

                # print(final_results)

                
                req_contact_list = []
                batch_ids = []
                print(len(final_results ))

                for i in final_results:
                    req_contact_list.append(i["mobile_number"])
                    batch_ids.append(i["batch_id"])

                # print(new_json_data)
                # print(req_contact_list)

                end_contact_list = []
                

                for c in range (len(req_contact_list)):
                    temp = req_contact_list[c][:12]
                    end_contact_list.append(temp)

                print(end_contact_list)
                print(batch_ids)



                # res = {
                #     'status': True,
                #     'message': 'Data fetched successfully.',
                #     'data': final_results
                # }
                # return Response(res, status=status.HTTP_200_OK)

                

                

                for c, b in zip(end_contact_list, batch_ids):

                    url = "https://live-server-2553.wati.io/api/v1/getMessages/{0}".format(c)

                    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0MzE5NjQxMC1iNDA2LTQ0ZDktOWFiYy1lZTE5ZmZiZWMzNWEiLCJ1bmlxdWVfbmFtZSI6IlNvbmFtQGtzbGVnYWwuY28uaW4iLCJuYW1laWQiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiZW1haWwiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiYXV0aF90aW1lIjoiMDgvMDMvMjAyMSAwNToyOToxNCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFETUlOSVNUUkFUT1IiLCJleHAiOjI1MzQwMjMwMDgwMCwiaXNzIjoiQ2xhcmVfQUkiLCJhdWQiOiJDbGFyZV9BSSJ9.d8Z083VdTnmkv4k86NTY6oU6PhRhEi_ldUc-7cHN9Sg"}

                    response = requests.request("GET", url, headers=headers)

                    r = response.json()

                    if response.status_code == 200 and r["result"]=="success":

                        

                        raw_df = pd.json_normalize(r["messages"],record_path=["items"])

                        raw_df["number"] = c
                        raw_df["batch_id"] = b

                        print(raw_df)

                        current_date = datetime.date.today().strftime("%Y-%m-%d")

                        final_dataframes_data = {}

                        for table in BATCH_TABLE_HELPER:
                            print('TABLE_NAME>>>', table)
                            not_found_fields = []
                            found_fields_data = {}

                            

                            for field in BATCH_TABLE_HELPER.get(table):

                                if field in raw_df.columns:
                                    
                                    found_fields_data.update({field: raw_df[field]})
                                    
                                else:
                                    not_found_fields.append(field) 

                            # print(found_fields_data)
                            # print(not_found_fields)
                            
                            temp_df = pd.DataFrame(data=found_fields_data)
                            temp_df['created_at'] = current_date
                            
                            for field in not_found_fields:
                                temp_df[field] = 'None'
                        #     print(temp_df.head())

                            

                            
                                
                            final_dataframes_data.update({
                                table: {
                                    "db_table_name": f"{table}_table",
                                    "write_path": get_write_path(table),
                                    "df": temp_df,
                                    "description": f"this is our {table} database table.",
                                    "dtype": DTYPES.get(table)
                                }
                            })
                            
                            
                        final_batch_meta_data = {
                        'batch_name': 'batch_name'
                        }

                        database = 'the_medius_database'

                        # temp2 = 'wAid'
                        # for key,val in data["contact_list"]:
                        #     if temp2 in val:
                        #         reso = [val[temp2]]
                    

                        for df in final_dataframes_data:
                            
                            
                            
                            
                            reponse = wr.s3.to_parquet(df=final_dataframes_data.get(df).get('df'), path=final_dataframes_data.get(df).get('write_path'), dataset=True, mode = 'append' , database=database, table=final_dataframes_data.get(df).get('db_table_name'), dtype=final_dataframes_data.get(df).get('dtype'), description=final_dataframes_data.get(df).get('description'))
                            uri_path = None
                            if len(reponse.get('paths')) > 0:
                                uri_path = reponse.get('paths')[0]
                            final_batch_meta_data.update({f"{df}_s3_uri": uri_path})

                        
                            # print(final_batch_meta_data)
                            
                            ConversationWati.objects.create(Conversation_Wati_s3_uri = final_batch_meta_data)


                get_contact_serializer = ConversationWatiSerializer(data=final_batch_meta_data)
                        # print(contact_serializer)
                if get_contact_serializer.is_valid():
                    batch_obj = get_contact_serializer.save()
                            
                else:
                    err_res = {
                                    'status': False,
                                    'message': get_contact_serializer.errors,
                                    'data': None
                                }
                    return Response(err_res, status=status.HTTP_200_OK)
                                    
                response = {
                                'status': True,
                                'message': 'Conversation data saved sucessfully.',
                                # 'data': r["contact_list"]
                            }
                return Response(response, status=status.HTTP_201_CREATED)


class GotConversationByAthena(APIView):
        def get(self, request, format=None):

                number_entered_by_user = request.query_params.get('number')

            # batch_id = self.request.query_params.get('batch_id')

            # if batch_id:
        
                S3_BUCKET = 'themedius.ai'

                client = boto3.client('athena')
                queryStart = client.start_query_execution(
                    QueryString = f"SELECT * FROM conversation_wati_table",
                    QueryExecutionContext = {
                        'Database': 'the_medius_database'
                    }, 
                    ResultConfiguration = { 'OutputLocation': 's3://themedius.ai/Batch_Database/'}
                )
                queryExecutionId = queryStart.get('QueryExecutionId')

                while True:
                    query_state = client.get_query_execution(QueryExecutionId=queryExecutionId).get('QueryExecution').get('Status').get('State')
                    print(query_state)
                    if query_state == 'SUCCEEDED' or query_state == 'FAILED' or query_state == 'CANCELLED':
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

                # Conversation_Wati
                # print(final_results)

                for i in final_results:
                    Conversation_Wati.objects.update_or_create(conversationId = i['conversation_id'], text = i['text'], created = i['created'], finalText = i['final_text'], owner = i['owner'],eventDescription = i['event_description'],number = i['number'] , batch_id = i['batch_id'],created_at = i['created_at'])

                if number_entered_by_user:
                        queryset = Conversation_Wati.objects.filter(number=number_entered_by_user).order_by('-created')
                else:
                        queryset = Conversation_Wati.objects.all().order_by('-created')

                serializer = Conversation_WatiSerializer(queryset, many=True)

                res = {
                    'status': True,
                    'message': 'Data fetched successfully.',
                    'data': serializer.data
                }
                return Response(res, status=status.HTTP_200_OK)


