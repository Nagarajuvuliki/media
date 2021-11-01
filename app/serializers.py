
from .models import Batch, Customer, Account, LastTransaction, Loan,Contacts,GetContacts,ConversationWati,Client,Convo_Wati_Acc_Numb,Conversation_Wati,CallingData1,Wati_Webhook
from rest_framework import serializers
from utils.customSerializers import DynamicFieldsModelSerializer, NestedSerializerField





class ClientSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'



class BatchSerializer(DynamicFieldsModelSerializer):
    client = NestedSerializerField(queryset=Client.objects.all(), serializer=ClientSerializer, custom_fields=('client_id', 'client_name'))

    class Meta:
        model = Batch
        fields = '__all__'


class CustomerSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class AccountSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class LastTransactionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = LastTransaction
        fields = '__all__'


class LoanSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'

class GetContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetContacts
        fields = '__all__'

class ConversationWatiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationWati
        fields = '__all__'

class Convo_Wati_Acc_NumbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convo_Wati_Acc_Numb
        fields = '__all__'

class Conversation_WatiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation_Wati
        fields = '__all__'

class CallingData1Serializer(serializers.ModelSerializer):
    class Meta:
        model = CallingData1
        fields = ['loan_account_no','customer_phone','batch_id','template_id','scheduled_at','name','due_amount','due_date','status','response','created_at','updated_at']


class Wati_WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wati_Webhook
        fields = '__all__'


batch_column_info = {
    "ZONE_NAME": "zone_name",
    "REGION_NAME": "region_name",
    "BRAN_CODE": "batch_code",
    "AREANAME": "first_name",
    "BRANACHNAME": "batch_name",
    "DUE_AGMTNO": "due_agmt_no",
    "TENOR": "tenor",
    "ADVEMI": "adv_emi",
    "MOB": "mob",
    "BKT": "bkt",
    "EMI": "emi",
    "DEMAND": "demand",
    "OVERDUE": "overdue",
    "TOTAL CHARGES": "total_charges",
    "TOTAL OD ( OD + CHARGES )": "total_od",
    "FUTURE_PRINC": "future_princ",
    "POS ( OD + FP )": "pos",
    "ADDRESS": "address1",
    "Mobile Number": "mobile_number",
    "Alternate Number": "alt_contact_number",
    "FIRST_EMI_DATE": "first_emi_date",
    "LAST_EMI_DATE": "last_emi_date",
    "AMOUNT_FINANACED": "amount_financed",
    "DISBURSAL_DATE": "disbursal_date",
    "PRODUCTGROUP": "product_group",
    "STATUS": "status",
    "PAYMENTTYPE": "payment_type",
    "CITY": "city",
    "PINCODE": "pincode",
    "LANDMARK": "landmark",
    "OFC_ADDRESS1": "office_address1",
    "OFC_ADDRESS2": "office_address2",
    "OFC_ADDRESS3": "office_address3",
    "OFC_PINCODE": "office_pincode",
    "OFC_MOBILENO": "office_mobile_number",
    "MODEL": "model",
    "REG_NUMBER": "reg_no",
    "CHASSIS_NO": "chassis_no",
    "ENG_NO": "eng_no",
    "LAST_COLL_DATE": "last_collection_date",
    "LTV": "ltv",
    "LOAN_AMOUNT": "loan_amount",
    "CUST_PROFILE": "customer_profile",
    "MORAT_TYPE": "morat_type"
}


dtype = {
    "zone_name": "string",
    "region_name": "string",
    "batch_code": "string",
    "first_name": "string",
    "batch_name": "string",
    "due_agmt_no": "string",
    "tenor": "string",
    "adv_emi": "string",
    "mob": "string",
    "bkt": "string",
    "emi": "string",
    "demand": "string",
    "overdue": "string",
    "total_charges": "string",
    "total_od": "string",
    "future_princ": "string",
    "pos": "string",
    "address1": "string",
    "mobile_number": "string",
    "alt_contact_number": "string",
    "first_emi_date": "string",
    "last_emi_date": "string",
    "amount_financed": "string",
    "disbursal_date": "string",
    "product_group": "string",
    "status": "string",
    "payment_type": "string",
    "city": "string",
    "pincode": "string",
    "landmark": "string",
    "office_address1": "string",
    "office_address2": "string",
    "office_address3": "string",
    "office_pincode": "string",
    "office_mobile_number": "string",
    "model": "string",
    "reg_no": "string",
    "chassis_no": "string",
    "eng_no": "string",
    "last_collection_date": "string",
    "ltv": "float",
    "loan_amount": "int",
    "customer_profile": "string",
    "morat_type": "string"
}