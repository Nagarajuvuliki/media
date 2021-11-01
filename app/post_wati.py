import awswrangler as wr
import pandas as pd
import boto3
import json
import datetime
from app.wati_helper_data import DTYPES 
from .models import Contacts
from .serializers import ContactSerializer
from django.db.models import Q
from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render
import requests

import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
# from app import serializers
from rest_framework.filters import SearchFilter




class WatiPostContact(APIView):

    def post(self,request,format=None):

        res = request.data

        print(res)
        result = json.dumps(res)
        print(type(result))


        if res['number'][:2] == "91" and len(res['number'])==12:   
            url = "https://live-server-2553.wati.io/api/v1/addContact/"+res['number']

        elif res['number'][0] == "0" and len(res['number']==11):
            res["number"] = res["number"][1:]
            url = "https://live-server-2553.wati.io/api/v1/addContact/91"+res['number']


        else:
            url = "https://live-server-2553.wati.io/api/v1/addContact/91"+res['number']

        payload = "{\"customParams\":[{\"name\":\""+res['name']+'\",\"value\":\"'+res['value']+"\"}],\"name\":\""+res['fullName']+"\"}"


        headers = {
            "Content-Type": "application/json-patch+json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4ODkxY2IzOC0zYmMyLTQ4Y2QtYTg1Ni1kMzU1NWVhZWVjNDAiLCJ1bmlxdWVfbmFtZSI6IlNvbmFtQGtzbGVnYWwuY28uaW4iLCJuYW1laWQiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiZW1haWwiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiYXV0aF90aW1lIjoiMDcvMzEvMjAyMSAwNTo0OToxNCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFETUlOSVNUUkFUT1IiLCJleHAiOjI1MzQwMjMwMDgwMCwiaXNzIjoiQ2xhcmVfQUkiLCJhdWQiOiJDbGFyZV9BSSJ9.Rb0BUVwOjbQC1WDY4GxoZivv2Dk2NSnUFwXDKyaJn90"
        }
        r = requests.request('POST', url, data=payload, headers=headers)
        try:
            data = r.json()

            print(data)

            print("~~~~~~~~~~~~")
            
            pls = res

            print(type(pls))

            print("~~~~~~~~~~~~")

            raw_df = pd.json_normalize(pls)

            print(raw_df)

            print("------")

            # print(raw_df)

            current_date = datetime.date.today().strftime("%Y-%m-%d")


            not_found_fields = []
            found_fields_data = {}

            for field in DTYPES:
                if field in raw_df.columns:
                    found_fields_data.update({field: raw_df[field]})
                    
                    
                else:
                    not_found_fields.append(field)
                    
                    

            final_df = pd.DataFrame(data=found_fields_data)
            final_df['created_at'] = current_date


            for field in not_found_fields:
                final_df[field] = 'None'
            print(final_df)

            now = datetime.datetime.now()
            current_year = now.year
            current_month = now.month

            final_batch_meta_data = {
                'batch_name': 'batch_name'
            }


            database = 'the_medius_database'
            BUCKET_NAME = 'themedius.ai'
            db_table_name = 'contacts_table'
            description = 'this is our contact table'

            write_path = f"s3://{BUCKET_NAME}/Batch_Database/Contacts"
            print(write_path)


            reponse = wr.s3.to_parquet(df=final_df, path=write_path, dataset=True, mode='append', database=database, table=db_table_name, dtype=DTYPES, description=description)
            uri_path = None
            if len(reponse.get('paths')) > 0:
                uri_path = reponse.get('paths')[0]
            final_batch_meta_data.update({"s3_uri": uri_path})
            


            contact_serializer = ContactSerializer(data=final_batch_meta_data)
            # print(contact_serializer)
            if contact_serializer.is_valid():
                batch_obj = contact_serializer.save()
            else:
                err_res = {
                        'status': False,
                        'message': contact_serializer.errors,
                        'data': None
                    }
                return Response(err_res, status=status.HTTP_200_OK)
                        
            response = {
                    'status': True,
                    'message': 'Contact data saved sucessfully.',
                    # 'data': {
                    #     'contact_uri': contact_serializer.data
                    # }
                }
            return Response(response, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("----------------")
            print(str(e))
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_200_OK)








