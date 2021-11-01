from typing import final
from rest_framework.pagination import Cursor
from .models import Customer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.authentication import TokenAuthentication
from  rest_framework.permissions import IsAuthenticated
import datetime
from .serializers import CustomerSerializer
import json
from utils.customPagination import CustomPagination, paginator_function
from dateutil.parser import parse





class AccountView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination


    def get(self, request, format=None):
        batch_id = self.request.query_params.get('batch_id')
        customer_id = self.request.query_params.get('customer_id')
        last_disposition = self.request.query_params.get('last_disposition')
        overdue = self.request.query_params.get('overdue')
        product = self.request.query_params.get('product')
        risk_status = self.request.query_params.get('status')
        amount_from = self.request.query_params.get('amount_from')
        amount_to = self.request.query_params.get('amount_to')
        sort = self.request.query_params.get('sort')

        if sort == 'asc':
            sort_by = 'customer_id'
        elif sort == 'desc':
            sort_by = '-customer_id'
        else:
            sort_by = '-customer_id'


        if customer_id:
            customer_data = Customer.objects.filter(customer_id=customer_id).first()
            serializer = CustomerSerializer(customer_data)

            res = {
                'status': True,
                'message': 'Account data fetched successfully.',
                'data': serializer.data
            }
            return Response(res, status=status.HTTP_200_OK)

        else:
            related_customers = Customer.objects.filter(batch__client__user=request.user).order_by(sort_by)
            
            if batch_id:
                related_customers = related_customers.filter(batch__batch_id=batch_id)
            else:
                related_customers = related_customers.filter(batch__client__user=request.user)
            if last_disposition:
                related_customers = related_customers.filter(last_disposition=last_disposition)
            if overdue:
                related_customers = related_customers.filter(due_days=overdue)
            if product:
                related_customers = related_customers.filter(product_name=product)
            if risk_status:
                related_customers = related_customers.filter(risk_status=risk_status)
            if amount_from and amount_to:
                related_customers = related_customers.filter(product_amount__range=[float(amount_from), float(amount_to)])


            paginated_data = paginator_function(self, related_customers)
            final_data = []
            for customer in paginated_data.get('data'):
                serializer = CustomerSerializer(customer, fields=('customer_id', 'customer_name', 'loan_account_no', 'customer_mobile_number', 'risk_status', 'due_date', 'last_disposition', 'assigned_date', 'first_called_date', 'last_disposition_date', 'emi', 'loan_amount', 'product_name'))
                final_data.append({**{'batch_id': customer.batch.batch_id}, **serializer.data})
            paginated_data.update({'data': final_data})
            res = {**{'status': True, 'message': 'Account data fetched successfully.'}, **paginated_data}

            return Response(res, status=status.HTTP_200_OK)
