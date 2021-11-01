from .models import Batch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dateutil.parser import parse
import xlrd
import datetime
from .serializers import BatchSerializer
import json

import awswrangler as wr
import pandas as pd
import boto3
from app.batchHelperData import DTYPES, BATCH_TABLE_HELPER



def get_write_path(table_name):
    dir_name = ""
    if table_name in ["customer", "customer_home_address", "customer_office_data", "emi_date_data", "customer_guarantor", "loan"]:
        dir_name = table_name
    return f"s3://themedius.ai/Batch_Database/{table_name}/"




class BatchView(APIView):
    def get(self, request, format=None):
        loan_account_number = self.request.query_params.get('loan_account_number')

        if loan_account_number:
            S3_BUCKET = 'themedius.ai'

            client = boto3.client('athena')
            queryStart = client.start_query_execution(
                QueryString = f"SELECT * FROM customer_home_address_table where loan_account_number='{loan_account_number}'",
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

            res = {
                'status': True,
                'message': 'Data fetched successfully.',
                'data': final_results
            }
            return Response(res, status=status.HTTP_200_OK)

        err_res = {
            'status': False,
            'message': 'Invalid loan_account_number.',
            'data': None
        }
        return Response(err_res, status=status.HTTP_400_BAD_REQUEST)




    def post(self, request, format=None):
        # batch_file = request.FILES.get('batch_file')
        # batch_name = request.POST.get('batch_name')
        # client_id = request.POST.get('client')
        # column_rename_data = request.POST.get('column_rename_data')
        # column_rename_data = json.loads(column_rename_data)
        # print(column_rename_data)
        body_unicode = request.body.decode('utf-8')
        body_decode = json.loads(body_unicode)
        client_id = body_decode.get('client')
 


        if True:
        # if batch_name and batch_file:
            # s3 = boto3.resource('s3')
            # try:
            #     object = s3.Object('themedius.ai', batch_file.name)
            #     object.put(ACL='public-read',Body=batch_file.read(), Key=f"uploaded_by_backend_{batch_file.name}")
            # except Exception as e:
            #     print('ERRRRRRRRRRRRRRRRRRRR', e)
            #     pass

            # raw_df = pd.read_excel(batch_file.file.seek(0).read())
            # current_date = datetime.date.today().strftime("%Y-%m-%d")
            # cleaned_df = raw_df.rename(columns=column_rename_data)

            # final_dataframes_data = {}

            # for table in BATCH_TABLE_HELPER:
            #     not_found_fields = []
            #     found_fields_data = {}

            #     for field in BATCH_TABLE_HELPER.get(table):
            #         if field in cleaned_df.columns:
            #             found_fields_data.update({field: cleaned_df[field]})
            #         else:
            #             not_found_fields.append(field)

                
            #     temp_df = pd.DataFrame(data=found_fields_data)
            #     temp_df['created_at'] = current_date
                
            #     for field in not_found_fields:
            #         temp_df[field] = 'None'
            #     # print(temp_df.head())
                    
            #     final_dataframes_data.update({
            #         table: {
            #             "db_table_name": f"{table}_table",
            #             "write_path": get_write_path(table),
            #             "df": temp_df,
            #             "description": f"this is our {table} database table.",
            #             "dtype": DTYPES.get(table)
            #         }
            #     })

            # final_batch_meta_data = {
            #     'batch_name': batch_name,
            #     'file': batch_file
            # }

            # database = 'the_medius_database'

            # for df in final_dataframes_data:
            #     print('SAVING ...',df)
                
            #     reponse = wr.s3.to_parquet(df=final_dataframes_data.get(df).get('df'), path=final_dataframes_data.get(df).get('write_path'), dataset=True, mode='append', database=database, table=final_dataframes_data.get(df).get('db_table_name'), dtype=final_dataframes_data.get(df).get('dtype'), description=final_dataframes_data.get(df).get('description'))
            #     uri_path = None
            #     if len(reponse.get('paths')) > 0:
            #         uri_path = reponse.get('paths')[0]
            #     final_batch_meta_data.update({f"{df}_s3_uri": uri_path})

            

            # batch_serializer = BatchSerializer(data=final_batch_meta_data)
            existing_batches_for_this_client = Batch.objects.filter(client=client_id).order_by('-batch_id')
            if existing_batches_for_this_client:
                new_batch_id = existing_batches_for_this_client[0].batch_id + 1
            else:
                new_batch_id = 1
            batch_serializer = BatchSerializer(data=request.data)
            if batch_serializer.is_valid():
                batch_obj = batch_serializer.save(batch_id=new_batch_id)
            else:
                err_res = {
                    'status': False,
                    'message': batch_serializer.errors,
                    'data': None
                }
                return Response(err_res, status=status.HTTP_200_OK)
                    
            response = {
                'status': True,
                'message': 'Batch data saved sucessfully.',
                'data': {
                    'batch': batch_serializer.data
                }
            }
            return Response(response, status=status.HTTP_201_CREATED)

        err_res = {
            'status': False,
            'message': 'Void batch_name or batch_file.',
            'data': None
        }
        return Response(err_res, status=status.HTTP_400_BAD_REQUEST)