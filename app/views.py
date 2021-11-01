# from .models import *
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, viewsets
# from django_filters  import rest_framework as filters
# from dateutil.parser import parse
# # import xlrd
# import datetime
# from .serializers import BatchSerializer, CustomerSerializer, AccountSerializer, LastTransactionSerializer, LoanSerializer
# from rest_framework.decorators import action
# import json


# class BatchFilter(filters.FilterSet):

#     class Meta:
#         model = Batch
#         fields = {
#             'batch_name': ['icontains'],
#             'dealer_name': ['icontains'],
#             'zone_name': ['icontains'],
#             'region_name': ['icontains'],
#             'area_name': ['icontains'],
#         }
# class BatchViewSet(viewsets.ModelViewSet):
#     queryset = Batch.objects.all()
#     serializer_class = BatchSerializer
#     filterset_class = BatchFilter

#     @action(methods=['get'], detail=False)
#     def newest(self, request):
#         newest = self.get_queryset().order_by('batch_id').last()
#         serializer = self.get_serializer_class()(newest)
#         return Response(serializer.data)

# class CustomerFilter(filters.FilterSet):

#     class Meta:
#         model = Customer
#         fields = {
#         'customer_id' : ['icontains'],
#         'first_name' : ['icontains'],
#         'last_name' : ['icontains'],
#         'address' : ['icontains'],
#         'email' :['icontains'],
#         'phone' :['icontains'],
#         'customer_created_at' :['icontains'],
#         'father_name' :['icontains'],
#         'customer_profile' :['icontains'],
#         'loan_acc_no' :['icontains'],
#         'due_prop_no' :['icontains'],
#         'due_agmt_no' :['icontains'],

#         }


# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#     filterset_class = CustomerFilter

#     @action(methods=['get'], detail=False)
#     def newest(self, request):
#         newest = self.get_queryset().order_by('customer_id').last()
#         serializer = self.get_serializer_class()(newest)
#         return Response(serializer.data)
# # from .models import *
# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status, viewsets
# # from django_filters  import rest_framework as filters
# # from dateutil.parser import parse
# # import xlrd
# # import datetime
# # from .serializers import BatchSerializer, CustomerSerializer, AccountSerializer, LastTransactionSerializer, LoanSerializer
# # from rest_framework.decorators import action
# # import json


# # class BatchFilter(filters.FilterSet):

# #     class Meta:
# #         model = Batch
# #         fields = {
# #             'batch_name': ['icontains'],
# #             'dealer_name': ['icontains'],
# #             'zone_name': ['icontains'],
# #             'region_name': ['icontains'],
# #             'area_name': ['icontains'],
# #         }
# # class BatchViewSet(viewsets.ModelViewSet):
# #     queryset = Batch.objects.all()
# #     serializer_class = BatchSerializer
# #     filterset_class = BatchFilter

# #     @action(methods=['get'], detail=False)
# #     def newest(self, request):
# #         newest = self.get_queryset().order_by('batch_id').last()
# #         serializer = self.get_serializer_class()(newest)
# #         return Response(serializer.data)

# # class CustomerFilter(filters.FilterSet):

# #     class Meta:
# #         model = Customer
# #         fields = {
# #         'customer_id' : ['icontains'],
# #         'first_name' : ['icontains'],
# #         'last_name' : ['icontains'],
# #         'address' : ['icontains'],
# #         'email' :['icontains'],
# #         'phone' :['icontains'],
# #         'customer_created_at' :['icontains'],
# #         'father_name' :['icontains'],
# #         'customer_profile' :['icontains'],
# #         'loan_acc_no' :['icontains'],
# #         'due_prop_no' :['icontains'],
# #         'due_agmt_no' :['icontains'],

# #         }


# # class CustomerViewSet(viewsets.ModelViewSet):
# #     queryset = Customer.objects.all()
# #     serializer_class = CustomerSerializer
# #     filterset_class = CustomerFilter

# #     @action(methods=['get'], detail=False)
# #     def newest(self, request):
# #         newest = self.get_queryset().order_by('customer_id').last()
# #         serializer = self.get_serializer_class()(newest)
# #         return Response(serializer.data)



# # # class BatchView(APIView):
# # #     def get(self, request, format=None):
# # #         pass

# # #     def post(self, request, format=None):
# # #         batch_file = request.FILES.get('batch_file')
# # #         batch_name = request.POST.get('batch_name')


# # #         if batch_name and batch_file:
# # #             workbook = xlrd.open_workbook(file_contents=batch_file.read())
# # #             # batch_obj = Batch.objects.create(batch_name=batch_name, file=batch_file)
# # #             batch_serializer = BatchSerializer(data={'batch_name': batch_name, 'file': batch_file})
# # #             if batch_serializer.is_valid():
# # #                 batch_obj = batch_serializer.save()
# # #             else:
# # #                 err_res = {
# # #                     'status': False,
# # #                     'message': batch_serializer.errors,
# # #                     'data': None
# # #                 }
# # #                 return Response(err_res, status=status.HTTP_200_OK)

# # #             for sheet in workbook.sheets():
# # #                 row_count = sheet.nrows
# # #                 col_count = sheet.ncols

# # #                 column_name_index_data = {}
# # #                 # temp = []
# # #                 customer_serialized_data = []
# # #                 account_serialized_data = []
# # #                 loan_serialized_data = []
# # #                 last_txn_serialized_data = []

# # #                 for row_index in range(row_count):
# # #                     row_data = {}
# # #                     for col_index in range(col_count):
# # #                         cell = sheet.cell(row_index, col_index)
# # #                         if row_index == 0:
# # #                             column_name_index_data.update({col_index: cell.value})
# # #                         else:
# # #                             if column_name_index_data.get(col_index) in ['customer_created_at', 'account_created_at']:
# # #                                 if isinstance(cell.value, float):
# # #                                     date_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(cell.value, workbook.datemode))
# # #                                     row_data.update({column_name_index_data.get(col_index): date_as_datetime.date().strftime("%Y-%m-%d")})
# # #                                 else:
# # #                                     row_data.update({column_name_index_data.get(col_index): parse(cell.value).strftime("%Y-%m-%d")})
# # #                             else:
# # #                                 row_data.update({column_name_index_data.get(col_index): cell.value})

# # #                     if row_index != 0:
# # #                         customer_serializer = CustomerSerializer(data={'first_name': row_data.get('first_name'), 'last_name': row_data.get('last_name'), 'address': row_data.get('address'), 'email': row_data.get('email'), 'phone': row_data.get('phone'), 'batch':batch_obj.batch_id, 'customer_created_at': row_data.get('customer_created_at')})
# # #                         if customer_serializer.is_valid():
# # #                             customer_obj = customer_serializer.save()

# # #                         # customer_obj = Customer.objects.create(first_name=row_data.get('first_name'), last_name=row_data.get('last_name'), address=row_data.get('address'), email=row_data.get('email'), phone=row_data.get('phone'), batch=batch_obj, customer_created_at=row_data.get('customer_created_at'))
# # #                         customer_serialized_data.append(customer_serializer.data)
# # #                         if row_data.get('account_number'):
# # #                             account_obj = Account.objects.create(account_number=int(row_data.get('account_number')), customer=customer_obj, account_type=row_data.get('account_type'), balance=row_data.get('balance'), account_created_at=row_data.get('account_created_at'))
# # #                             account_serialized_data.append(AccountSerializer(account_obj).data)
# # #                         if row_data.get('transaction_number'):
# # #                             last_txn_obj = LastTransaction.objects.create(transaction_number=int(row_data.get('transaction_number')), transaction_amount=row_data.get('transaction_amount'), customer=customer_obj)
# # #                             last_txn_serialized_data.append(LastTransactionSerializer(last_txn_obj).data)
# # #                         if row_data.get('loan_account_number'):
# # #                             loan_obj = Loan.objects.create(loan_account_number=int(row_data.get('loan_account_number')), loan_amount=row_data.get('loan_amount'), customer=customer_obj)
# # #                             loan_serialized_data.append(LoanSerializer(loan_obj).data)
# # #             #             temp.append(row_data)
# # #             # print(temp)

# # #             response = {
# # #                 'status': True,
# # #                 'message': 'Data saved sucessfully.',
# # #                 'data': {
# # #                     'batch': batch_serializer.data,
# # #                     'customer': customer_serialized_data,
# # #                     'account': account_serialized_data,
# # #                     'last_transaction': last_txn_serialized_data,
# # #                     'loan': loan_serialized_data
# # #                 }
# # #             }
# # #             return Response(response, status=status.HTTP_201_CREATED)

# # #         err_res = {
# # #             'status': False,
# # #             'message': 'Void batch_name or batch_file.',
# # #             'data': None
# # #         }
# # #         return Response(err_res, status=status.HTTP_400_BAD_REQUEST)






# # class BatchView(APIView):
# #     def get(self, request, format=None):
# #         pass

# #     def post(self, request, format=None):
# #         batch_file = request.FILES.get('batch_file')
# #         batch_name = request.POST.get('batch_name')
# #         batch_column_info = request.POST.get('batch_column_info')
# #         batch_column_info = json.loads(batch_column_info)
# #         print(batch_column_info)
# #         # return None
# #         # batch_column_info = {
# #         #     'fa_name': 'first_name'
# #         # }
# #         BATCH_SIZE = 500

# #         if batch_name and batch_file:
# #             workbook = xlrd.open_workbook(file_contents=batch_file.read())
# #             batch_serializer = BatchSerializer(data={'batch_name': batch_name, 'file': batch_file})
# #             if batch_serializer.is_valid():
# #                 batch_obj = batch_serializer.save()
# #             else:
# #                 err_res = {
# #                     'status': False,
# #                     'message': batch_serializer.errors,
# #                     'data': None
# #                 }
# #                 return Response(err_res, status=status.HTTP_200_OK)
    

# #             for sheet in workbook.sheets():
# #                 row_count = sheet.nrows
# #                 col_count = sheet.ncols

# #                 column_name_index_data = {}
# <<<<<<< HEAD
# #                 # temp = []
# #                 customer_serialized_data = []
# #                 account_serialized_data = []
# #                 loan_serialized_data = []
# #                 last_txn_serialized_data = []

# #                 for row_index in range(row_count):
# #                     row_data = {}
# #                     for col_index in range(col_count):
# #                         cell = sheet.cell(row_index, col_index)
# #                         if row_index == 0:
# #                             column_name_index_data.update({col_index: cell.value})
# #                         else:
# #                             if column_name_index_data.get(col_index) in ['customer_created_at', 'account_created_at']:
# #                                 if isinstance(cell.value, float):
# #                                     date_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(cell.value, workbook.datemode))
# #                                     row_data.update({column_name_index_data.get(col_index): date_as_datetime.date().strftime("%Y-%m-%d")})
# #                                 else:
# #                                     row_data.update({column_name_index_data.get(col_index): parse(cell.value).strftime("%Y-%m-%d")})
# #                             else:
# #                                 row_data.update({column_name_index_data.get(col_index): cell.value})

# #                     if row_index != 0:
# #                         customer_serializer = CustomerSerializer(data={'first_name': row_data.get('first_name'), 'last_name': row_data.get('last_name'), 'address': row_data.get('address'), 'email': row_data.get('email'), 'phone': row_data.get('phone'), 'batch':batch_obj.batch_id, 'customer_created_at': row_data.get('customer_created_at')})
# #                         if customer_serializer.is_valid():
# #                             customer_obj = customer_serializer.save()

# #                         # customer_obj = Customer.objects.create(first_name=row_data.get('first_name'), last_name=row_data.get('last_name'), address=row_data.get('address'), email=row_data.get('email'), phone=row_data.get('phone'), batch=batch_obj, customer_created_at=row_data.get('customer_created_at'))
# #                         customer_serialized_data.append(customer_serializer.data)
# #                         if row_data.get('account_number'):
# #                             account_obj = Account.objects.create(account_number=int(row_data.get('account_number')), customer=customer_obj, account_type=row_data.get('account_type'), balance=row_data.get('balance'), account_created_at=row_data.get('account_created_at'))
# #                             account_serialized_data.append(AccountSerializer(account_obj).data)
# #                         if row_data.get('transaction_number'):
# #                             last_txn_obj = LastTransaction.objects.create(transaction_number=int(row_data.get('transaction_number')), transaction_amount=row_data.get('transaction_amount'), customer=customer_obj)
# #                             last_txn_serialized_data.append(LastTransactionSerializer(last_txn_obj).data)
# #                         if row_data.get('loan_account_number'):
# #                             loan_obj = Loan.objects.create(loan_account_number=int(row_data.get('loan_account_number')), loan_amount=row_data.get('loan_amount'), customer=customer_obj)
# #                             loan_serialized_data.append(LoanSerializer(loan_obj).data)
# #             #             temp.append(row_data)
# #             # print(temp)

# #             response = {
# #                 'status': True,
# #                 'message': 'Data saved sucessfully.',
# #                 'data': {
# #                     'batch': batch_serializer.data,
# #                     'customer': customer_serialized_data,
# #                     'account': account_serialized_data,
# #                     'last_transaction': last_txn_serialized_data,
# #                     'loan': loan_serialized_data
# #                 }
# #             }
# #             return Response(response, status=status.HTTP_201_CREATED)

# #         err_res = {
# #             'status': False,
# #             'message': 'Void batch_name or batch_file.',
# #             'data': None
# #         }
# #         return Response(err_res, status=status.HTTP_400_BAD_REQUEST)





# #
# # class BatchView(APIView):
# #     def get(self, request, format=None):
# #         pass
# #
# #     def post(self, request, format=None):
# #         batch_file = request.FILES.get('batch_file')
# #         batch_name = request.POST.get('batch_name')
# #         batch_column_info = request.POST.get('batch_column_info')
# #         batch_column_info = json.loads(batch_column_info)
# #         print(batch_column_info)
# #         # return None
# #         # batch_column_info = {
# #         #     'fa_name': 'first_name'
# #         # }
# #         BATCH_SIZE = 500
# #
# #         if batch_name and batch_file:
# #             workbook = xlrd.open_workbook(file_contents=batch_file.read())
# #             batch_serializer = BatchSerializer(data={'batch_name': batch_name, 'file': batch_file})
# #             if batch_serializer.is_valid():
# #                 batch_obj = batch_serializer.save()
# #             else:
# #                 err_res = {
# #                     'status': False,
# #                     'message': batch_serializer.errors,
# #                     'data': None
# #                 }
# #                 return Response(err_res, status=status.HTTP_200_OK)
# #
# #
# #             for sheet in workbook.sheets():
# #                 row_count = sheet.nrows
# #                 col_count = sheet.ncols
# #
# #                 column_name_index_data = {}
# #                 account_batch = []
# #                 customer_home_address_batch = []
# #                 customer_office_address_batch = []
# #                 customer_guarantor_batch = []
# #                 source_batch = []
# #                 risk_batch = []
# #                 collection_agent_batch = []
# #                 product_batch = []
# #                 emi_date_batch = []
# #                 loan_batch = []
# #                 for row_index in range(row_count):
# #                     row_data = {}
# #                     for col_index in range(col_count):
# #                         cell = sheet.cell(row_index, col_index)
# #                         if row_index == 0:
# #                             if str(cell.value) in batch_column_info:
# #                                 column_name_index_data.update({col_index: batch_column_info.get(cell.value)})
# #                             else:
# #                                 column_name_index_data.update({col_index: cell.value})
# #                         else:
# #                             if column_name_index_data.get(col_index) in ['customer_created_at', 'account_created_at', 'agreement_data', 'disbursal_date', 'last_collection_date', 'first_emi_date', 'last_emi_date'] and cell.value is not None:
# #                                 if isinstance(cell.value, float):
# #                                     date_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(cell.value, workbook.datemode))
# #                                     row_data.update({column_name_index_data.get(col_index): date_as_datetime.date().strftime("%Y-%m-%d")})
# #                                 elif "-" in str(cell.value) or "/" in str(cell.value) or "\\" in str(cell.value):
# #                                     row_data.update({column_name_index_data.get(col_index): parse(cell.value).strftime("%Y-%m-%d")})
# #                                 else:
# #                                     row_data.update({column_name_index_data.get(col_index): None})
# #                             else:
# #                                 row_data.update({column_name_index_data.get(col_index): cell.value})
# #
# #                     if row_index != 0:
# #                         print(row_data.get('SL NO'))
# #                         customer_serializer = CustomerSerializer(data={'first_name': row_data.get('first_name'), 'last_name': row_data.get('last_name'), 'address': row_data.get('address'), 'email': row_data.get('email'), 'phone': row_data.get('phone'), 'batch':batch_obj.batch_id, 'raw_data':json.dumps(row_data), 'customer_created_at': row_data.get('customer_created_at')})
# #                         if customer_serializer.is_valid(): #first_name last_name address email phone
# #                             customer_obj = customer_serializer.save()
# #
# #                             account_batch.append(Account(account_number=row_data.get('account_number'), customer=customer_obj, account_type=row_data.get('account_type'), balance=row_data.get('balance'), account_created_at=row_data.get('account_created_at')))
# #                             customer_home_address_batch.append(CustomerHomeAddress(pincode=row_data.get('pincode'), landmark=row_data.get('landmark'), address1=row_data.get('address1'), address2=row_data.get('address2'), address3=row_data.get('address3'), customer=customer_obj, city=row_data.get('city'), state=row_data.get('state'), region=row_data.get('region'), zone=row_data.get('zone'), mobile_number=row_data.get('mobile_number'), alt_contact_number=row_data.get('alt_contact_number')))
# #                             customer_office_address_batch.append(CustomerOffice(office_pincode=row_data.get('office_pincode'), office_landmark=row_data.get('office_landmark'), office_address1=row_data.get('office_address1'), office_address2=row_data.get('office_address2'), office_address3=row_data.get('office_address3'), customer=customer_obj, office_city=row_data.get('office_city'), office_state=row_data.get('office_state'), office_region=row_data.get('office_region'), office_zone=row_data.get('office_zone'), office_mobile_number=row_data.get('office_mobile_number')))
# #                             customer_guarantor_batch.append(CustomerGuarantor(guarantor_name=row_data.get('guarantor_name'), gur_address1=row_data.get('gur_address1'), gur_address2=row_data.get('gur_address2'), gur_address3=row_data.get('gur_address3'), customer=customer_obj, gur_city=row_data.get('gur_city'), gur_landmark=row_data.get('gur_landmark'), gur_pincode=row_data.get('gur_pincode')))
# #                             source_batch.append(Source_details(source_proposal=row_data.get('source_proposal'), source_tw_dealer_code=row_data.get('source_tw_dealer_code'), source_tw_dealer_name=row_data.get('source_tw_dealer_name'), customer=customer_obj))
# #                             risk_batch.append(Risk(pre_bnc_risk_seg=row_data.get('pre_bnc_risk_seg'), post_bnc_risk_seg=row_data.get('post_bnc_risk_seg'), bounce_prediction=row_data.get('bounce_prediction'), od_prediction=row_data.get('od_prediction'), customer=customer_obj, repo_risk_flag=row_data.get('repo_risk_flag'), expected_loss=row_data.get('expected_loss')))
# #                             collection_agent_batch.append(CollectionAgent(asc_code=row_data.get('asc_code'), asc_name=row_data.get('asc_name'), collector_code=row_data.get('collector_code'), collector_name=row_data.get('collector_name'), customer=customer_obj, sec_name=row_data.get('sec_name'), territory_manager=row_data.get('territory_manager')))
# #                             product_batch.append(Product(portfolio=row_data.get('portfolio'), product_group=row_data.get('product_group'), business_portfolio=row_data.get('business_portfolio'), customer=customer_obj, product_code=row_data.get('product_code'), model=row_data.get('model'), reg_no=row_data.get('reg_no'), chassis_no=row_data.get('chassis_no'), eng_no=row_data.get('eng_no')))
# #                             emi_date_batch.append(EmiDate(disbursal_date=row_data.get('disbursal_date'), last_collection_date=row_data.get('last_collection_date'), first_emi_date=row_data.get('first_emi_date'), last_emi_date=row_data.get('last_emi_date'), agening=row_data.get('agening'), last_collection_gap_category=row_data.get('last_collection_gap_category'), cheque_bounce=row_data.get('cheque_bounce'), cash_bounce=row_data.get('cash_bounce'), score_category=row_data.get('score_category'), customer=customer_obj, segment=row_data.get('segment'), od_movement=row_data.get('od_movement'), unmatured_tenor=row_data.get('unmatured_tenor'), opening_dpd=row_data.get('opening_dpd'), current_dpd_bracket=row_data.get('current_dpd_bracket'), payment_frequency=row_data.get('payment_frequency'), dpd_del_string=row_data.get('dpd_del_string'), closing_dpd=row_data.get('closing_dpd'), closing_dpd_bracket=row_data.get('closing_dpd_bracket')))
# #                             loan_batch.append(Loan(loan_account_number=row_data.get('loan_account_number'), loan_amount=row_data.get('loan_amount'), customer=customer_obj, agreement_data=row_data.get('agreement_data'), lrn=row_data.get('lrn'), tenor=row_data.get('tenor'), adv_emi=row_data.get('adv_emi'), mob=row_data.get('mob'), bkt=row_data.get('bkt'), emi=row_data.get('emi'), demand=row_data.get('demand'), receivable=row_data.get('receivable'), received=row_data.get('received'), overdue=row_data.get('overdue'), total_charges=row_data.get('total_charges'), total_od=row_data.get('total_od'), future_princ=row_data.get('future_princ'), pos=row_data.get('pos'), amount_financed=row_data.get('amount_financed'), ltv=row_data.get('ltv'), morat_type=row_data.get('morat_type'), status=row_data.get('status'), payment_type=row_data.get('payment_type'), insurance_type=row_data.get('insurance_type'), cbd_receivable=row_data.get('cbd_receivable'), cbd_received=row_data.get('cbd_received'), cbd_waived=row_data.get('cbd_waived'), cbc_due=row_data.get('cbc_due'), afc_receivable=row_data.get('afc_receivable'), afc_received=row_data.get('afc_received'), afc_waived=row_data.get('afc_waived'), afc_due=row_data.get('afc_due'), cash_bnc_receivable=row_data.get('cash_bnc_receivable'), cash_bnc_received=row_data.get('cash_bnc_received'), cash_bnc_waived=row_data.get('cash_bnc_waived'), cash_bnc_due=row_data.get('cash_bnc_due'), ins_receivable=row_data.get('ins_receivable'), ins_received=row_data.get('ins_received'), ins_due=row_data.get('ins_due'), clearing_receivable=row_data.get('clearing_receivable'), clearing_received=row_data.get('clearing_received'), clearing_due=row_data.get('clearing_due'), od_collectable=row_data.get('od_collectable'), demand_collectable=row_data.get('demand_collectable'), future_outstanding=row_data.get('future_outstanding'), asset_cost=row_data.get('asset_cost'), scheme_code=row_data.get('scheme_code'), scheme_name=row_data.get('scheme_name')))
# #
# #
# #                         else:
# #                             print('/////*******************//*******************//********>>>>>>>>>>>>>>>>>>>>>>??????////',customer_serializer.errors)
# #
# #                         if row_index % BATCH_SIZE == 0 or row_index == row_count:
# #                             print('wahh wahh....DATA PUSHEDDDDD>>>')
# #                             Account.objects.bulk_create(account_batch, BATCH_SIZE)
# #                             CustomerHomeAddress.objects.bulk_create(customer_home_address_batch, BATCH_SIZE)
# #                             CustomerOffice.objects.bulk_create(customer_office_address_batch, BATCH_SIZE)
# #                             CustomerGuarantor.objects.bulk_create(customer_guarantor_batch, BATCH_SIZE)
# #                             Source_details.objects.bulk_create(source_batch, BATCH_SIZE)
# #                             Risk.objects.bulk_create(risk_batch, BATCH_SIZE)
# #                             CollectionAgent.objects.bulk_create(collection_agent_batch, BATCH_SIZE)
# #                             Product.objects.bulk_create(product_batch, BATCH_SIZE)
# #                             EmiDate.objects.bulk_create(emi_date_batch, BATCH_SIZE)
# #                             Loan.objects.bulk_create(loan_batch, BATCH_SIZE)
# #
# #                             account_batch *= 0
# #                             customer_home_address_batch *= 0
# #                             customer_office_address_batch *= 0
# #                             customer_guarantor_batch *= 0
# #                             source_batch *= 0
# #                             risk_batch *= 0
# #                             collection_agent_batch *= 0
# #                             product_batch *= 0
# #                             emi_date_batch *= 0
# #                             loan_batch *= 0
# #                             print('>>>EMPTYING THE BATCHES..', account_batch)
# #
# #
# =======
#                 account_batch = []
#                 customer_home_address_batch = []
#                 customer_office_address_batch = []
#                 customer_guarantor_batch = []
#                 source_batch = []
#                 risk_batch = []
#                 collection_agent_batch = []
#                 product_batch = []
#                 emi_date_batch = []
#                 loan_batch = []
#                 for row_index in range(row_count):
#                     row_data = {}
#                     for col_index in range(col_count):
#                         cell = sheet.cell(row_index, col_index)
#                         if row_index == 0:
#                             if str(cell.value) in batch_column_info:
#                                 column_name_index_data.update({col_index: batch_column_info.get(cell.value)})
#                             else:
#                                 column_name_index_data.update({col_index: cell.value})
#                         else:
#                             if column_name_index_data.get(col_index) in ['customer_created_at', 'account_created_at', 'agreement_data', 'disbursal_date', 'last_collection_date', 'first_emi_date', 'last_emi_date'] and cell.value is not None:
#                                 if isinstance(cell.value, float):
#                                     date_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(cell.value, workbook.datemode))
#                                     row_data.update({column_name_index_data.get(col_index): date_as_datetime.date().strftime("%Y-%m-%d")})
#                                 elif "-" in str(cell.value) or "/" in str(cell.value) or "\\" in str(cell.value):
#                                     row_data.update({column_name_index_data.get(col_index): parse(cell.value).strftime("%Y-%m-%d")})
#                                 else:
#                                     row_data.update({column_name_index_data.get(col_index): None})
#                             else:
#                                 row_data.update({column_name_index_data.get(col_index): cell.value})

#                     if row_index != 0:
#                         print(row_data.get('SL NO'))
#                         customer_serializer = CustomerSerializer(data={'first_name': row_data.get('first_name'), 'last_name': row_data.get('last_name'), 'address': row_data.get('address'), 'email': row_data.get('email'), 'phone': row_data.get('phone'), 'batch':batch_obj.batch_id, 'raw_data':json.dumps(row_data), 'customer_created_at': row_data.get('customer_created_at')})
#                         if customer_serializer.is_valid(): #first_name last_name address email phone 
#                             customer_obj = customer_serializer.save()
            
#                             account_batch.append(Account(account_number=row_data.get('account_number'), customer=customer_obj, account_type=row_data.get('account_type'), balance=row_data.get('balance'), account_created_at=row_data.get('account_created_at')))
#                             customer_home_address_batch.append(CustomerHomeAddress(pincode=row_data.get('pincode'), landmark=row_data.get('landmark'), address1=row_data.get('address1'), address2=row_data.get('address2'), address3=row_data.get('address3'), customer=customer_obj, city=row_data.get('city'), state=row_data.get('state'), region=row_data.get('region'), zone=row_data.get('zone'), mobile_number=row_data.get('mobile_number'), alt_contact_number=row_data.get('alt_contact_number')))
#                             customer_office_address_batch.append(CustomerOffice(office_pincode=row_data.get('office_pincode'), office_landmark=row_data.get('office_landmark'), office_address1=row_data.get('office_address1'), office_address2=row_data.get('office_address2'), office_address3=row_data.get('office_address3'), customer=customer_obj, office_city=row_data.get('office_city'), office_state=row_data.get('office_state'), office_region=row_data.get('office_region'), office_zone=row_data.get('office_zone'), office_mobile_number=row_data.get('office_mobile_number')))
#                             customer_guarantor_batch.append(CustomerGuarantor(guarantor_name=row_data.get('guarantor_name'), gur_address1=row_data.get('gur_address1'), gur_address2=row_data.get('gur_address2'), gur_address3=row_data.get('gur_address3'), customer=customer_obj, gur_city=row_data.get('gur_city'), gur_landmark=row_data.get('gur_landmark'), gur_pincode=row_data.get('gur_pincode')))
#                             source_batch.append(Source_details(source_proposal=row_data.get('source_proposal'), source_tw_dealer_code=row_data.get('source_tw_dealer_code'), source_tw_dealer_name=row_data.get('source_tw_dealer_name'), customer=customer_obj))
#                             risk_batch.append(Risk(pre_bnc_risk_seg=row_data.get('pre_bnc_risk_seg'), post_bnc_risk_seg=row_data.get('post_bnc_risk_seg'), bounce_prediction=row_data.get('bounce_prediction'), od_prediction=row_data.get('od_prediction'), customer=customer_obj, repo_risk_flag=row_data.get('repo_risk_flag'), expected_loss=row_data.get('expected_loss')))
#                             collection_agent_batch.append(CollectionAgent(asc_code=row_data.get('asc_code'), asc_name=row_data.get('asc_name'), collector_code=row_data.get('collector_code'), collector_name=row_data.get('collector_name'), customer=customer_obj, sec_name=row_data.get('sec_name'), territory_manager=row_data.get('territory_manager')))
#                             product_batch.append(Product(portfolio=row_data.get('portfolio'), product_group=row_data.get('product_group'), business_portfolio=row_data.get('business_portfolio'), customer=customer_obj, product_code=row_data.get('product_code'), model=row_data.get('model'), reg_no=row_data.get('reg_no'), chassis_no=row_data.get('chassis_no'), eng_no=row_data.get('eng_no')))
#                             emi_date_batch.append(EmiDate(disbursal_date=row_data.get('disbursal_date'), last_collection_date=row_data.get('last_collection_date'), first_emi_date=row_data.get('first_emi_date'), last_emi_date=row_data.get('last_emi_date'), agening=row_data.get('agening'), last_collection_gap_category=row_data.get('last_collection_gap_category'), cheque_bounce=row_data.get('cheque_bounce'), cash_bounce=row_data.get('cash_bounce'), score_category=row_data.get('score_category'), customer=customer_obj, segment=row_data.get('segment'), od_movement=row_data.get('od_movement'), unmatured_tenor=row_data.get('unmatured_tenor'), opening_dpd=row_data.get('opening_dpd'), current_dpd_bracket=row_data.get('current_dpd_bracket'), payment_frequency=row_data.get('payment_frequency'), dpd_del_string=row_data.get('dpd_del_string'), closing_dpd=row_data.get('closing_dpd'), closing_dpd_bracket=row_data.get('closing_dpd_bracket')))
#                             loan_batch.append(Loan(loan_account_number=row_data.get('loan_account_number'), loan_amount=row_data.get('loan_amount'), customer=customer_obj, agreement_data=row_data.get('agreement_data'), lrn=row_data.get('lrn'), tenor=row_data.get('tenor'), adv_emi=row_data.get('adv_emi'), mob=row_data.get('mob'), bkt=row_data.get('bkt'), emi=row_data.get('emi'), demand=row_data.get('demand'), receivable=row_data.get('receivable'), received=row_data.get('received'), overdue=row_data.get('overdue'), total_charges=row_data.get('total_charges'), total_od=row_data.get('total_od'), future_princ=row_data.get('future_princ'), pos=row_data.get('pos'), amount_financed=row_data.get('amount_financed'), ltv=row_data.get('ltv'), morat_type=row_data.get('morat_type'), status=row_data.get('status'), payment_type=row_data.get('payment_type'), insurance_type=row_data.get('insurance_type'), cbd_receivable=row_data.get('cbd_receivable'), cbd_received=row_data.get('cbd_received'), cbd_waived=row_data.get('cbd_waived'), cbc_due=row_data.get('cbc_due'), afc_receivable=row_data.get('afc_receivable'), afc_received=row_data.get('afc_received'), afc_waived=row_data.get('afc_waived'), afc_due=row_data.get('afc_due'), cash_bnc_receivable=row_data.get('cash_bnc_receivable'), cash_bnc_received=row_data.get('cash_bnc_received'), cash_bnc_waived=row_data.get('cash_bnc_waived'), cash_bnc_due=row_data.get('cash_bnc_due'), ins_receivable=row_data.get('ins_receivable'), ins_received=row_data.get('ins_received'), ins_due=row_data.get('ins_due'), clearing_receivable=row_data.get('clearing_receivable'), clearing_received=row_data.get('clearing_received'), clearing_due=row_data.get('clearing_due'), od_collectable=row_data.get('od_collectable'), demand_collectable=row_data.get('demand_collectable'), future_outstanding=row_data.get('future_outstanding'), asset_cost=row_data.get('asset_cost'), scheme_code=row_data.get('scheme_code'), scheme_name=row_data.get('scheme_name')))

                            
#                         else: 
#                             print('/////*******************//*******************//********>>>>>>>>>>>>>>>>>>>>>>??????////',customer_serializer.errors)

#                         if row_index % BATCH_SIZE == 0 or row_index == row_count:
#                             print('wahh wahh....DATA PUSHEDDDDD>>>')
#                             Account.objects.bulk_create(account_batch, BATCH_SIZE)
#                             CustomerHomeAddress.objects.bulk_create(customer_home_address_batch, BATCH_SIZE)
#                             CustomerOffice.objects.bulk_create(customer_office_address_batch, BATCH_SIZE)
#                             CustomerGuarantor.objects.bulk_create(customer_guarantor_batch, BATCH_SIZE)
#                             Source_details.objects.bulk_create(source_batch, BATCH_SIZE)
#                             Risk.objects.bulk_create(risk_batch, BATCH_SIZE)
#                             CollectionAgent.objects.bulk_create(collection_agent_batch, BATCH_SIZE)
#                             Product.objects.bulk_create(product_batch, BATCH_SIZE)
#                             EmiDate.objects.bulk_create(emi_date_batch, BATCH_SIZE)
#                             Loan.objects.bulk_create(loan_batch, BATCH_SIZE)
  
#                             account_batch *= 0
#                             customer_home_address_batch *= 0
#                             customer_office_address_batch *= 0
#                             customer_guarantor_batch *= 0
#                             source_batch *= 0
#                             risk_batch *= 0
#                             collection_agent_batch *= 0
#                             product_batch *= 0
#                             emi_date_batch *= 0
#                             loan_batch *= 0
#                             print('>>>EMPTYING THE BATCHES..', account_batch)
                    
       
# >>>>>>> 31b8b36591b661800d18b9400caf955d8b4f7dc9
# #             response = {
# #                 'status': True,
# #                 'message': 'Data saved sucessfully.',
# #                 'data': {
# #                     'batch': batch_serializer.data
# #                     # 'customer': customer_serialized_data,
# #                     # 'account': account_serialized_data,
# #                     # 'last_transaction': last_txn_serialized_data,
# #                     # 'loan': loan_serialized_data
# #                 }
# #             }
# #             return Response(response, status=status.HTTP_201_CREATED)
# <<<<<<< HEAD
# #
# =======

# >>>>>>> 31b8b36591b661800d18b9400caf955d8b4f7dc9
# #         err_res = {
# #             'status': False,
# #             'message': 'Void batch_name or batch_file.',
# #             'data': None
# #         }
# #         return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
# <<<<<<< HEAD
# #
# #
# #
# =======



# >>>>>>> 31b8b36591b661800d18b9400caf955d8b4f7dc9

from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.serializers import Serializer
from app.helper1 import get_c_no
import requests
from .models import Convo_Wati_Acc_Numb,CallingData1,Wati_Webhook
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import Convo_Wati_Acc_NumbSerializer,CallingData1Serializer,Wati_WebhookSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

contact_numbers = get_c_no()

def save_conversations_acc_numb(request):
    for c in contact_numbers:


        url = "https://live-server-2553.wati.io/api/v1/getMessages/{0}".format(c)

        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0MzE5NjQxMC1iNDA2LTQ0ZDktOWFiYy1lZTE5ZmZiZWMzNWEiLCJ1bmlxdWVfbmFtZSI6IlNvbmFtQGtzbGVnYWwuY28uaW4iLCJuYW1laWQiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiZW1haWwiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiYXV0aF90aW1lIjoiMDgvMDMvMjAyMSAwNToyOToxNCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFETUlOSVNUUkFUT1IiLCJleHAiOjI1MzQwMjMwMDgwMCwiaXNzIjoiQ2xhcmVfQUkiLCJhdWQiOiJDbGFyZV9BSSJ9.d8Z083VdTnmkv4k86NTY6oU6PhRhEi_ldUc-7cHN9Sg"}

        response = requests.request("GET", url, headers=headers)

        r = response.json()

        if response.status_code == 200 and r["result"]=="success":

            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            for i in range (len(r["messages"]["items"])):

                if len(r["messages"]["items"][i]) == 12:

                    # print("Wati Template Message : \n")
                    # print(r["messages"]["items"][i]["finalText"])
                    # print("\n")

                    Convo_Wati_Acc_Numb.objects.update_or_create(number=c,conversation = r["messages"]["items"][i]["finalText"],From = "Wati Template Message" ,To = "User", created = r["messages"]["items"][i]["created"]) 

                elif len(r["messages"]["items"][i]) == 19 and r["messages"]["items"][i]["owner"] == False:

                    # print("User Message : \n")
                    # print(r["messages"]["items"][i]["text"])
                    # print("\n")

                    Convo_Wati_Acc_Numb.objects.update_or_create(number=c,conversation = r["messages"]["items"][i]["text"],From = "User" ,To = "Wati",created = r["messages"]["items"][i]["created"]) 


                elif len(r["messages"]["items"][i]) == 19 and r["messages"]["items"][i]["owner"] == True:

                    # print("Wati Message : \n")
                    # print(r["messages"]["items"][i]["text"])
                    # print("\n")
                    Convo_Wati_Acc_Numb.objects.update_or_create(number=c,conversation = r["messages"]["items"][i]["text"],From = "Wati" ,To = "User",created = r["messages"]["items"][i]["created"]) 

                else:
                    pass


         
            # print("--------------------")
    return JsonResponse({"status": "success"})

    
    
    # return HttpResponse("Failed")

class conversations_api_acc_numb(APIView):

    def get(self,request,format=None):
        
        number_entered_by_user = request.query_params.get('number')
        if number_entered_by_user:
            queryset = Convo_Wati_Acc_Numb.objects.filter(number=number_entered_by_user).order_by('-created')
        else:
            # queryset = Conversation.objects.all().order_by('-sent')
            queryset = Convo_Wati_Acc_Numb.objects.all().order_by('-created')
        serializer = Convo_Wati_Acc_NumbSerializer(queryset,many = True)
        # filterset_fields = ['number','name','status']

        response = {
                'status': True,
                'message': 'Data fetched successfully.',
                'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_msg_from_wati(request):
                if request.method == "POST":
                    res = request.data



                    url = "https://live-server-2553.wati.io/api/v1/sendSessionMessage/"+res['number']
                  
                    querystring = {"messageText":res['message']}
                   
                    headers = {
                        "Content-Type": "application/json-patch+json",
                        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4ODkxY2IzOC0zYmMyLTQ4Y2QtYTg1Ni1kMzU1NWVhZWVjNDAiLCJ1bmlxdWVfbmFtZSI6IlNvbmFtQGtzbGVnYWwuY28uaW4iLCJuYW1laWQiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiZW1haWwiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiYXV0aF90aW1lIjoiMDcvMzEvMjAyMSAwNTo0OToxNCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFETUlOSVNUUkFUT1IiLCJleHAiOjI1MzQwMjMwMDgwMCwiaXNzIjoiQ2xhcmVfQUkiLCJhdWQiOiJDbGFyZV9BSSJ9.Rb0BUVwOjbQC1WDY4GxoZivv2Dk2NSnUFwXDKyaJn90"
                    }

                    

                    r = requests.request("POST", url, headers=headers, params=querystring)
                    if r.status_code == 200:
                        data = r.json()
                        
                        return Response(data, status=status.HTTP_200_OK)
                    return Response({"error": "Request failed"}, status=r.status_code)
                else:
                    return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerData(APIView):
    def get(self,request,format=None):
        queryset = CallingData1.objects.all()
        serializer = CallingData1Serializer(queryset,many = True)
        response = {
                'status': True,
                'message': 'Data fetched successfully.',
                'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

class Wati_Webhook_View(APIView):
    def post(self, request, format=None):
        res = str(request.data)
        webhook_serializer = Wati_WebhookSerializer(data={'webhook': res})
        if webhook_serializer.is_valid():
            serializer = webhook_serializer.save()
            response = {
                'status': True,
                'message': 'Data saved sucessfully.',
                'data': {
                    'webhook': webhook_serializer.data

                }
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            err_res = {
                'status': False,
                'message': webhook_serializer.errors,
                'data': None
            }
            return Response(err_res, status=status.HTTP_200_OK)













