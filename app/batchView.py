from typing import final
import requests
from .models import Batch, BatchAttachment, Client, Customer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.authentication import TokenAuthentication
from  rest_framework.permissions import IsAuthenticated
from dateutil.parser import parse
import datetime
from .serializers import BatchSerializer
import json
import awswrangler as wr
import pandas as pd
import boto3
from app.batchHelperData import DTYPES
from utils.customPagination import CustomPagination, paginator_function





class BatchView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination



    def get(self, request, format=None):
        batch_id = self.request.query_params.get('batch_id')
        batch_name = self.request.query_params.get('batch_name')
        batch_status = self.request.query_params.get('batch_status')
        to_date = self.request.query_params.get('to_date')
        from_date = self.request.query_params.get('from_date')
        specific_date = self.request.query_params.get('specific_date')
        sort = self.request.query_params.get('sort')

        if sort == 'asc':
            sort_by = 'batch_id'
        elif sort == 'desc':
            sort_by = '-batch_id'
        else:
            sort_by = '-batch_id'


        if from_date and to_date:
            from_date = parse(from_date).strftime('%Y-%m-%d')
            to_date = parse(to_date).strftime('%Y-%m-%d')
     
        if specific_date:
            specific_date = parse(specific_date).strftime('%Y-%m-%d')

        
        related_batch = Batch.objects.filter(client__user=request.user).order_by(sort_by)
        if batch_id:
            related_batch = related_batch.filter(batch_id=batch_id)
        if batch_name:
            related_batch = related_batch.filter(batch_name=batch_name)
        if batch_status:
            related_batch = related_batch.filter(batch_status=batch_status)
        if specific_date:
            related_batch = related_batch.filter(uploaded_date=specific_date)
        if to_date and from_date:
            related_batch = related_batch.filter(uploaded_date__range=[from_date, to_date])


        total_batches = related_batch.distinct('batch_id')

        statics_data = []
        for batch in total_batches:
            temp = {
                'batch_id': batch.batch_id,
                'total': {
                    'accounts': 0,
                    'amount': 0
                }
            }
            customer_in_batch = Customer.objects.filter(batch=batch.id)

            prevent_duplicate_products = []
            for customer in customer_in_batch:
                if customer.product_name:
                    product_name = customer.product_name.lower()

                    if product_name not in prevent_duplicate_products:
                        temp.update({product_name: {'accounts': 1, 'amount': float(customer.loan_amount)}})
                        prevent_duplicate_products.append(product_name)
                    else:
                        temp.update({product_name: {'accounts': temp.get(product_name).get('accounts') + 1, 'amount': temp.get(product_name).get('amount') + float(customer.loan_amount)}})
                    temp.update({'total': {'accounts': temp.get('total').get('accounts') + 1, 'amount': temp.get('total').get('amount') + float(customer.loan_amount)}})

            statics_data.append(temp)


        paginated_data = paginator_function(self, related_batch, serializer = BatchSerializer)
        res = {**{'status': True, 'message': 'Batch data fetched successfully.'}, **paginated_data, **{'statics_data': statics_data}}
 
        return Response(res, status=status.HTTP_200_OK)




    def post(self, request, format=None):
        batch_file = request.FILES.get('batch_file')
        batch_name = request.POST.get('batch_name')
        column_rename_data = request.POST.get('column_rename_data')
        column_rename_data = json.loads(column_rename_data)
        
        try:
            client = Client.objects.get(user=request.user.user_id)
            client_id = client.client_id
        except:
            err_res = {
                'status': False,
                'message': 'No client associated with current user.',
                'data': None
            }
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)

        if batch_name and batch_file:
            now = datetime.datetime.now()
            current_year = now.year
            current_month = now.month

            database = 'the_medius_database'
            BUCKET_NAME = 'themedius.ai'
            db_table_name = 'batch_table'
            description = 'this is our batch table'


            file_obj = BatchAttachment.objects.create(file=batch_file)
            s3 = boto3.resource('s3')
            try:
                object = s3.Object('themedius.ai', batch_file.name)
                uri = f"raw_files/batch/{current_year}/{current_month}/raw_{batch_file.name}"
                object.put(ACL='public-read', Body=batch_file.read(), Key=uri)
                uri = f"s3://{BUCKET_NAME}/" + uri
            except Exception as e:
                uri = ''

            existing_batches_for_this_client = Batch.objects.filter(client=client_id).order_by('-batch_id')
            if existing_batches_for_this_client:
                new_batch_id = existing_batches_for_this_client[0].batch_id + 1
            else:
                new_batch_id = 1

            # Trigger channels API url which in turn trigger 3 more APIs
            url = f'https://api.themedius.ai/dashboard/api/trigger_channels/?batch_id={new_batch_id}'
            # Current logged in user token
            token = request.user.authorization_token
            # Headers to be passed (for authentication) with API request
            headers = {
                'Authorization': f'Token {token}'
            }

            try:
                requests.get(url=url, headers=headers)
            except Exception as e:
                print(str(e))
                pass


            batch_obj = Batch.objects.create(batch_name=batch_name, batch_id=new_batch_id, raw_file=uri, client=client)

            raw_df = pd.read_excel(file_obj.file.read())
            current_date = datetime.date.today().strftime("%Y-%m-%d")
            cleaned_df = raw_df.rename(columns=column_rename_data)

            not_found_fields = []
            found_fields_data = {}
            for field in DTYPES:
                if field in cleaned_df.columns:
                    found_fields_data.update({field: cleaned_df[field]})
                else:
                    not_found_fields.append(field)

            final_df = pd.DataFrame(data=found_fields_data)

            for field in not_found_fields:
                final_df[field] = 'None'

            final_df['created_at'] = current_date
            final_df['client_id'] = client_id
            final_df['batch_id'] = new_batch_id
            final_df['year'] = current_year
            final_df['month'] = current_month
            final_df['risk_status'] = 'High'

            write_path = f"s3://{BUCKET_NAME}/batch_data/"
            reponse = wr.s3.to_parquet(df=final_df, path=write_path, dataset=True, mode='append', database=database, table=db_table_name, dtype=DTYPES, description=description, partition_cols=['client_id', 'year', 'month'])
            uri_path = None


            if len(reponse.get('paths')) > 0:
                uri_path = reponse.get('paths')[0]
            

            batch_obj.parquet_file = uri_path
            batch_obj.save()
            file_obj.delete()

            batch_serializer = BatchSerializer(batch_obj)

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





class TriggerChannels(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        batch_id = kwargs.get('batch_id')

        # URLs for the APIs to hit GET request with batch_id
        import_batch_url = f'https://api.themedius.ai/dashboard/api/import_batch/?batch_id={batch_id}&client_id=1'
        get_message_url = f'https://api.themedius.ai/message91/api/get_message_converjations_by_batch_id/{batch_id}/'
        send_message_url = f'https://api.themedius.ai/message91/api/send_message/{batch_id}'

        # current logged in user_token
        token = request.user.token

        # Headers to be passed (for authentication) with API request
        headers = {
            'Authorization': f'Token {token}'
        }

        try:
            requests.get(url=import_batch_url, headers=headers)
        except Exception as e:
            print(str(e))
            pass
        try:
            requests.get(url=get_message_url, headers=headers)
        except Exception as e:
            print(str(e))
            pass
        try:
            requests.post(url=send_message_url, headers=headers)
        except Exception as e:
            print(str(e))
            pass



        

def find_bucket_key(s3_path):
    s3_components = s3_path.split('/')
    bucket = s3_components[0]
    s3_key = ""
    if len(s3_components) > 1:
        s3_key = '/'.join(s3_components[1:])
    return bucket, s3_key


def split_s3_bucket_key(s3_path):
    if s3_path.startswith('s3://'):
        s3_path = s3_path[5:]
    return find_bucket_key(s3_path)





class BatchDownloadView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )



    def get(self, request, format=None):
        batch_id = self.request.query_params.get('batch_id')
 
        
        if batch_id:
            related_batch = Batch.objects.filter(client__user=request.user, batch_id=batch_id).first()

            if related_batch:
                if related_batch.raw_file and 's3://' in related_batch.raw_file:
                    bucket, key = split_s3_bucket_key(related_batch.raw_file)
                    s3 = boto3.client('s3')

                    url = s3.generate_presigned_url(
                        ClientMethod='get_object',
                        Params={
                            'Bucket': 'bucket',
                            'Key': 'key'
                        },
                        ExpiresIn = 120 # this file url expires in 120 seconds
                    )

                    res = {
                        'status': True, 
                        'message': 'Downlable url fetched successfully.',
                        'data': {
                            'url': url
                        }
                    }
                    return Response(res, status=status.HTTP_200_OK)

            res = {
                'status': True, 
                'message': 'Requested file not found.',
                'data': {}
            }
            return Response(res, status=status.HTTP_200_OK)

        err_res = {
            'status': False, 
            'message': 'void batch_id.',
            'data': None
        }
        return Response(err_res, status=status.HTTP_400_BAD_REQUEST)

