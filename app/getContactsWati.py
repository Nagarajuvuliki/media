from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render
import awswrangler as wr
import pandas as pd
import boto3
import json
import datetime


import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status
import requests
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from app import serializers
from rest_framework.filters import SearchFilter
from app.get_wati_helper import DTYPES 
from .models import GetContacts
from .serializers import GetContactSerializer



class Save_Contacts_S3(APIView):
    def get(self, request, format=None):


            url = "https://live-server-2553.wati.io/api/v1/getContacts"


            headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0MzE5NjQxMC1iNDA2LTQ0ZDktOWFiYy1lZTE5ZmZiZWMzNWEiLCJ1bmlxdWVfbmFtZSI6IlNvbmFtQGtzbGVnYWwuY28uaW4iLCJuYW1laWQiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiZW1haWwiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiYXV0aF90aW1lIjoiMDgvMDMvMjAyMSAwNToyOToxNCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFETUlOSVNUUkFUT1IiLCJleHAiOjI1MzQwMjMwMDgwMCwiaXNzIjoiQ2xhcmVfQUkiLCJhdWQiOiJDbGFyZV9BSSJ9.d8Z083VdTnmkv4k86NTY6oU6PhRhEi_ldUc-7cHN9Sg"}

            response = requests.request("GET", url, headers=headers)

            if response.status_code == 200:


                data = response.json()

                raw_df = pd.json_normalize(data,record_path=["contact_list"])

                print(raw_df)
                print("-------")

                current_date = datetime.date.today().strftime("%Y-%m-%d")


                not_found_fields = []
                found_fields_data = {}


                for field in DTYPES:
                    if field in raw_df.columns:
                        found_fields_data.update({field: raw_df[field]})
                        
                        
                        

                final_df = pd.DataFrame(data=found_fields_data)
                final_df['created_at'] = current_date

                print(final_df)


                now = datetime.datetime.now()
                current_year = now.year
                current_month = now.month

                final_batch_meta_data = {
                    'batch_name': 'batch_name'
                }


                database = 'the_medius_database'
                BUCKET_NAME = 'themedius.ai'
                db_table_name = 'get_contacts_table'
                description = 'this is our contact table'

                write_path = f"s3://{BUCKET_NAME}/Batch_Database/GetContacts"
                print(write_path)

                reponse = wr.s3.to_parquet(df=final_df, path=write_path, dataset=True, mode='append', database=database, table=db_table_name, dtype=DTYPES, description=description)
                uri_path = None
                if len(reponse.get('paths')) > 0:
                    uri_path = reponse.get('paths')[0]
                final_batch_meta_data.update({"s3_uri": uri_path})


                get_contact_serializer = GetContactSerializer(data=final_batch_meta_data)
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
                        'message': 'Contact data saved sucessfully.',
                        # 'data': data["contact_list"]
                    }
                return Response(response, status=status.HTTP_201_CREATED)

class GetContacts(APIView):
    def get(self, request, format=None):
        # w_aid = self.request.query_params.get('w_aid')
        # print(w_aid)

        # if w_aid:
            S3_BUCKET = 'themedius.ai'

            client = boto3.client('athena')
            queryStart = client.start_query_execution(
                QueryString = f"SELECT * FROM get_contacts_table ",
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

                    print(type(final_results))

            res = {
                'status': True,
                'message': 'Data fetched successfully.',
                'data': final_results
            }
            return Response(res, status=status.HTTP_200_OK)

        # err_res = {
        #     'status': False,
        #     'message': 'Invalid loan_account_number.',
        #     'data': None
        # }
        # return Response(err_res, status=status.HTTP_400_BAD_REQUEST)


