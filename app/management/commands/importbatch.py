from os import stat
from django.core.management.base import BaseCommand, CommandError
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Batch
from app.models import *
import boto3
import json
from rest_framework import  status
from app.serializers import *
from rest_framework.authentication import TokenAuthentication
from  rest_framework.permissions import IsAuthenticated
from dateutil.parser import parse



BUCKET = "themedius.ai"

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('batch_args', nargs='+', type=int)


    def handle(self, *args, **options):
        if len(options['batch_args']) == 2:
            batch_id = options['batch_args'][0]
            client_id = options['batch_args'][1]

            batch_obj = Batch.objects.filter(batch_id=batch_id, client=client_id).first()

            client = boto3.client('athena')
            queryStart = client.start_query_execution(
                QueryString = f"SELECT * FROM batch_table where batch_id={batch_id} AND client_id={client_id}",
                QueryExecutionContext = {
                    'Database': 'the_medius_database'
                }, 
                ResultConfiguration = { 'OutputLocation': 's3://themedius.ai/Batch_Database/'}
            )
            queryExecutionId = queryStart.get('QueryExecutionId')

            while True:
                query_state = client.get_query_execution(QueryExecutionId=queryExecutionId).get('QueryExecution').get('Status').get('State')
                if query_state == 'SUCCEEDED' or query_state == 'FAILED' or query_state == 'CANCELLED':
                    print('breakkkinggg...')
                    break

            if query_state == 'SUCCEEDED':
                results = client.get_query_results(QueryExecutionId=queryExecutionId)

                column_mapper = {}
                processed_data = []

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
                        processed_data.append(temp)
    
                print(processed_data)
                BATCH_SIZE = 10

                # account_batch = []
                # customer_home_address_batch = []
                length = len(processed_data)
                for index in range(length):
                    if index < 11:
                        row_data = processed_data[index]
                        customer_serializer = CustomerSerializer(data={'customer_name': row_data.get('customer_name'), 'product_name': row_data.get('product_name'), 'product_amount': row_data.get('product_amount'), 'due_days': row_data.get('due_days'), 'risk_status': row_data.get('risk_status'), 'batch':batch_obj.id, 'last_disposition': row_data.get('last_disposition'), 'assigned_date': row_data.get('assigned_date'), 'first_called_date': row_data.get('first_called_date'), 'last_disposition_date': row_data.get('last_disposition_date')})
                        if customer_serializer.is_valid():
                            customer_obj = customer_serializer.save()


                        # account_batch.append(Account(account_number=row_data.get('account_number'), customer=customer_obj, account_type=row_data.get('account_type'), balance=row_data.get('balance'), account_created_at=row_data.get('account_created_at')))
                        # customer_home_address_batch.append(CustomerHomeAddress(pincode=row_data.get('pincode'), landmark=row_data.get('landmark'), address1=row_data.get('address1'), address2=row_data.get('address2'), address3=row_data.get('address3'), customer=customer_obj, city=row_data.get('city'), state=row_data.get('state'), region=row_data.get('region'), zone=row_data.get('zone'), mobile_number=row_data.get('mobile_number'), alt_contact_number=row_data.get('alt_contact_number')))

                        if index % BATCH_SIZE == 0 or index == length:
                            print('DATA PUSHEDDDDD>>>')
                            # Account.objects.bulk_create(account_batch, BATCH_SIZE)
                            # CustomerHomeAddress.objects.bulk_create(customer_home_address_batch, BATCH_SIZE)
                                
                            # account_batch *= 0
                            # customer_home_address_batch *= 0


                self.stdout.write(self.style.ERROR('/** IMPORTED THE BATCH DATA OF BATCH_ID  : %s **/' % str(batch_id)))
                self.stdout.write(self.style.SUCCESS('Imported the batch data of batch_id...'))
                    


class ImportBatchView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )



    def get(self, request, format=None):
        batch_id = self.request.query_params.get('batch_id')
        client_id = self.request.query_params.get('client_id')

        if batch_id and client_id:
            batch_obj = Batch.objects.filter(batch_id=batch_id, client=client_id).first()

            client = boto3.client('athena')
            queryStart = client.start_query_execution(
                QueryString = f"SELECT * FROM batch_table where batch_id={batch_id} AND client_id={client_id}",
                QueryExecutionContext = {
                    'Database': 'the_medius_database'
                }, 
                ResultConfiguration = { 'OutputLocation': 's3://themedius.ai/Batch_Database/'}
            )
            queryExecutionId = queryStart.get('QueryExecutionId')

            while True:
                query_state = client.get_query_execution(QueryExecutionId=queryExecutionId).get('QueryExecution').get('Status').get('State')
                if query_state == 'SUCCEEDED' or query_state == 'FAILED' or query_state == 'CANCELLED':
                    print('breakkkinggg...')
                    break

            if query_state == 'SUCCEEDED':
                results = client.get_query_results(QueryExecutionId=queryExecutionId)

                column_mapper = {}
                processed_data = []

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
                                if column_mapper.get(i) in ['due_date']:
                                    if list(fields['Data'][i].values())[0] and list(fields['Data'][i].values())[0] != 'None':
                                        this_data = parse(list(fields['Data'][i].values())[0]).strftime('%Y-%m-%d')
                                    else:
                                        continue
                                elif column_mapper.get(i) in ['last_disposition_date', 'first_called_date', 'assigned_date']:
                                    continue
                                else:
                                    this_data = list(fields['Data'][i].values())[0]

                                temp.update({column_mapper.get(i): this_data})
                            else:
                                temp.update({column_mapper.get(i): 'None'})
                        processed_data.append(temp)

                # print(processed_data)
                BATCH_SIZE = 10

                # account_batch = []
                # customer_home_address_batch = []
                length = len(processed_data)
                for index in range(length):
                    if index < 11 or True:
                        row_data = processed_data[index]
                        # customer_serializer = CustomerSerializer(data={'customer_name': row_data.get('customer_name'), 'product_name': row_data.get('product_name'), 'product_amount': row_data.get('product_amount'), 'due_days': row_data.get('due_days'), 'risk_status': row_data.get('risk_status'), 'batch':batch_obj.id, 'last_disposition': row_data.get('last_disposition'), 'assigned_date': row_data.get('assigned_date'), 'first_called_date': row_data.get('first_called_date'), 'last_disposition_date': row_data.get('last_disposition_date')})
                        customer_serializer = CustomerSerializer(data=row_data)
                        
                        if customer_serializer.is_valid():
                            customer_obj = customer_serializer.save(batch=batch_obj)

                        # print(customer_serializer.errors)
                        # account_batch.append(Account(account_number=row_data.get('account_number'), customer=customer_obj, account_type=row_data.get('account_type'), balance=row_data.get('balance'), account_created_at=row_data.get('account_created_at')))
                        # customer_home_address_batch.append(CustomerHomeAddress(pincode=row_data.get('pincode'), landmark=row_data.get('landmark'), address1=row_data.get('address1'), address2=row_data.get('address2'), address3=row_data.get('address3'), customer=customer_obj, city=row_data.get('city'), state=row_data.get('state'), region=row_data.get('region'), zone=row_data.get('zone'), mobile_number=row_data.get('mobile_number'), alt_contact_number=row_data.get('alt_contact_number')))

                        if index % BATCH_SIZE == 0 or index == length:
                            print('DATA PUSHEDDDDD>>>')
                            # Account.objects.bulk_create(account_batch, BATCH_SIZE)
                            # CustomerHomeAddress.objects.bulk_create(customer_home_address_batch, BATCH_SIZE)
                                
                            # account_batch *= 0
                            # customer_home_address_batch *= 0

                res = {
                    'status': True,
                    'message': 'Batch data has been imprted successfully.',
                    'data': None
                }
                return Response(res, status=status.HTTP_200_OK)
        else:
            err_res = {
                'status': True,
                'message': 'void batch_id or client_id.',
                'data': None
            }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
