from django.db import models
import datetime

from django.db.models.fields import BooleanField
from account.models import User
import os
from django.conf import settings


class Client(models.Model):
    # client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=500)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_client',null=True,blank=True)

    def __str__(self):
        return self.client_name


class Batch(models.Model):
    # id = models.AutoField(primary_key=True)
    batch_name = models.CharField(max_length=500)
    batch_id = models.BigIntegerField(default=0)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    batch_status = models.CharField(max_length=50, default="new")
    total_account = models.BigIntegerField(default=0)
    total_connected = models.FloatField(default=0)
    total_ptp = models.FloatField(default=0)
    total_broken_ptp = models.FloatField(default=0)
    total_paid = models.FloatField(default=0)
    total_amount = models.TextField(null=True, blank=True)
    agent_count = models.IntegerField(default=1)
    raw_file = models.TextField(null=True, blank=True)
    parquet_file = models.TextField(null=True, blank=True)
    latest_updated_file = models.TextField(null=True, blank=True)
    uploaded_date = models.DateField(default=datetime.date.today)


    def __str__(self) :
        return f"{self.id} - {str(self.batch_name)}"




class Customer(models.Model): # customer_name product_name product_amount batch due_days risk_status last_disposition assigned_date first_called_date last_disposition_date
    # customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=500,null=True, blank=True)
    product_name = models.CharField(max_length=500,null=True, blank=True)
    product_amount = models.FloatField(null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    risk_status = models.CharField(max_length=500,null=True)
    last_disposition = models.CharField(max_length=500,null=True, blank=True)
    assigned_date = models.DateField(null=True, blank=True)
    first_called_date = models.DateField(null=True, blank=True)
    last_disposition_date = models.DateField(null=True, blank=True)
    loan_account_no = models.CharField(max_length=500, null=True, blank=True)

    zone_name = models.CharField(max_length=500, null=True, blank=True)
    region_name = models.CharField(max_length=500, null=True, blank=True)
    area_name = models.CharField(max_length=500, null=True, blank=True)
    branch_name = models.CharField(max_length=500, null=True, blank=True)
    branch_code = models.CharField(max_length=500, null=True, blank=True)
    dealer_code = models.CharField(max_length=500, null=True, blank=True)
    dealer_name = models.CharField(max_length=500, null=True, blank=True)
    father_name = models.CharField(max_length=500, null=True, blank=True)
    customer_profile = models.CharField(max_length=500, null=True, blank=True)
    due_prop_no = models.CharField(max_length=500, null=True, blank=True)
    due_agmt_no = models.CharField(max_length=500, null=True, blank=True)
    customer_landmark = models.CharField(max_length=500, null=True, blank=True)
    customer_address1 = models.TextField(null=True, blank=True)
    customer_address2 = models.TextField(null=True, blank=True)
    customer_address3 = models.TextField(null=True, blank=True)
    customer_city = models.CharField(max_length=500, null=True, blank=True)
    customer_state = models.CharField(max_length=500, null=True, blank=True)
    customer_region = models.CharField(max_length=500, null=True, blank=True)
    customer_zone = models.CharField(max_length=500, null=True, blank=True)
    customer_pincode = models.CharField(max_length=500, null=True, blank=True)
    customer_mobile_number = models.CharField(max_length=500, null=True, blank=True)
    customer_alt_contact_no = models.CharField(max_length=500, null=True, blank=True)
    office_pincode = models.CharField(max_length=500, null=True, blank=True)
    office_landmark = models.CharField(max_length=500, null=True, blank=True)
    office_address1 = models.TextField(null=True, blank=True)
    office_address2 = models.TextField(null=True, blank=True)
    office_address3 = models.TextField(null=True, blank=True)
    office_city = models.CharField(max_length=500, null=True, blank=True)
    office_state = models.CharField(max_length=500, null=True, blank=True)
    office_region = models.CharField(max_length=500, null=True, blank=True)
    office_zone = models.CharField(max_length=500, null=True, blank=True)
    office_pincode = models.CharField(max_length=500, null=True, blank=True)
    office_mobile_no = models.CharField(max_length=500, null=True, blank=True)
    guarantor_name = models.CharField(max_length=500, null=True, blank=True)
    guarantor_address1 = models.TextField(null=True, blank=True)
    guarantor_address2 = models.TextField(null=True, blank=True)
    guarantor_address3 = models.TextField(null=True, blank=True)
    guarantor_city = models.CharField(max_length=500, null=True, blank=True)
    guarantor_landmark = models.CharField(max_length=500, null=True, blank=True)
    guarantor_pincode = models.CharField(max_length=500, null=True, blank=True)
    agreement_date = models.CharField(max_length=500, null=True, blank=True)
    lrn = models.CharField(max_length=500, null=True, blank=True)
    tenor = models.CharField(max_length=500, null=True, blank=True)
    adv_emi = models.CharField(max_length=500, null=True, blank=True)
    mob = models.CharField(max_length=500, null=True, blank=True)
    bkt = models.CharField(max_length=500, null=True, blank=True)
    emi = models.CharField(max_length=500, null=True, blank=True)
    demand = models.CharField(max_length=500, null=True, blank=True)
    receivable = models.CharField(max_length=500, null=True, blank=True)
    received = models.CharField(max_length=500, null=True, blank=True)
    over_due = models.CharField(max_length=500, null=True, blank=True)
    total_charges = models.CharField(max_length=500, null=True, blank=True)
    total_od = models.CharField(max_length=500, null=True, blank=True)  #( OD + CHARGES )
    future_princ = models.CharField(max_length=500, null=True, blank=True)
    pos = models.CharField(max_length=500, null=True, blank=True)  #( OD + FP )
    amount_finanaced = models.CharField(max_length=500, null=True, blank=True)	
    ltv = models.CharField(max_length=500, null=True, blank=True)	
    loan_amount = models.CharField(max_length=500, null=True, blank=True)
    morat_type = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=500, null=True, blank=True)
    payment_type = models.CharField(max_length=500, null=True, blank=True)
    insurance_type = models.CharField(max_length=500, null=True, blank=True)
    cbd_receivable = models.CharField(max_length=500, null=True, blank=True)
    cbd_received = models.CharField(max_length=500, null=True, blank=True)
    cbd_waived = models.CharField(max_length=500, null=True, blank=True)
    cbc_due = models.CharField(max_length=500, null=True, blank=True)
    afc_receivable = models.CharField(max_length=500, null=True, blank=True)
    afc_received = models.CharField(max_length=500, null=True, blank=True)
    afc_waived = models.CharField(max_length=500, null=True, blank=True)
    afc_due = models.CharField(max_length=500, null=True, blank=True)
    cash_bnc_receivable = models.CharField(max_length=500, null=True, blank=True)
    cash_bnc_received = models.CharField(max_length=500, null=True, blank=True)
    cash_bnc_waived = models.CharField(max_length=500, null=True, blank=True)
    cash_bnc_due = models.CharField(max_length=500, null=True, blank=True)
    ins_receivable = models.CharField(max_length=500, null=True, blank=True)
    ins_received = models.CharField(max_length=500, null=True, blank=True)
    ins_due = models.CharField(max_length=500, null=True, blank=True)
    clearing_receivable = models.CharField(max_length=500, null=True, blank=True)
    clearing_received = models.CharField(max_length=500, null=True, blank=True)
    clearing_due = models.CharField(max_length=500, null=True, blank=True)
    od_collectable = models.CharField(max_length=500, null=True, blank=True)
    demand_collectable = models.CharField(max_length=500, null=True, blank=True)
    future_outstanding = models.CharField(max_length=500, null=True, blank=True)
    asset_cost = models.CharField(max_length=500, null=True, blank=True)
    scheme_code = models.CharField(max_length=500, null=True, blank=True)
    scheme_name = models.CharField(max_length=500, null=True, blank=True)
    source_proposal = models.CharField(max_length=500, null=True, blank=True)
    source_tw_dealer_code = models.CharField(max_length=500, null=True, blank=True)
    source_tw_dealer_name = models.CharField(max_length=500, null=True, blank=True)
    disbursal_date = models.CharField(max_length=500, null=True, blank=True)
    last_collection_date = models.CharField(max_length=500, null=True, blank=True)
    first_emi_date = models.CharField(max_length=500, null=True, blank=True)
    last_emi_date = models.CharField(max_length=500, null=True, blank=True)
    agening = models.CharField(max_length=500, null=True, blank=True)
    last_collection_gap_category = models.CharField(max_length=500, null=True, blank=True)
    cheque_bounce = models.CharField(max_length=500, null=True, blank=True)
    cash_bounce = models.CharField(max_length=500, null=True, blank=True)
    score_category = models.CharField(max_length=500, null=True, blank=True)
    segment = models.CharField(max_length=500, null=True, blank=True)
    od_movement = models.CharField(max_length=500, null=True, blank=True)
    unmatured_tenor = models.CharField(max_length=500, null=True, blank=True)
    opening_dpd = models.CharField(max_length=500, null=True, blank=True)
    opening_dpd_bracket = models.CharField(max_length=500, null=True, blank=True)
    payment_frequency = models.CharField(max_length=500, null=True, blank=True)
    dpd_del_string = models.CharField(max_length=500, null=True, blank=True)
    closing_dpd = models.CharField(max_length=500, null=True, blank=True)
    closing_dpd_bracket = models.CharField(max_length=500, null=True, blank=True)
    pre_bnc_risk_seg = models.CharField(max_length=500, null=True, blank=True)
    post_bnc_risk_seg = models.CharField(max_length=500, null=True, blank=True)
    bounce_prediction = models.CharField(max_length=500, null=True, blank=True)
    od_prediction = models.CharField(max_length=500, null=True, blank=True)
    repo_risk_flag = models.CharField(max_length=500, null=True, blank=True)
    expected_loss = models.CharField(max_length=500, null=True, blank=True)
    asc_code = models.CharField(max_length=500, null=True, blank=True)
    asc_name = models.CharField(max_length=500, null=True, blank=True)
    collector_code = models.CharField(max_length=500, null=True, blank=True)
    collector_name = models.CharField(max_length=500, null=True, blank=True)
    sce_name = models.CharField(max_length=500, null=True, blank=True)
    territory_manager = models.CharField(max_length=500, null=True, blank=True)
    # portfolio = models.CharField(max_length=500, null=True, blank=True)
    product_group = models.CharField(max_length=500, null=True, blank=True)
    business_portfolio = models.CharField(max_length=500, null=True, blank=True)
    product_code = models.CharField(max_length=500, null=True, blank=True)
    model = models.CharField(max_length=500, null=True, blank=True)
    reg_number = models.CharField(max_length=500, null=True, blank=True)
    chassis_no = models.CharField(max_length=500, null=True, blank=True)
    eng_no = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return f"{self.id} - {str(self.customer_name)}"

current_date_and_time = datetime.datetime.now()
hours = 2
hours_added = datetime.timedelta(hours = hours)

future_date_and_time = current_date_and_time + hours_added

class CallingData1(models.Model):
    # id = models.AutoField(primary_key=True)
    loan_account_no = models.CharField(max_length=500,null=True)
    customer_phone = models.CharField(max_length=500,null=True)
    call_attempt = models.IntegerField(default=0)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True)
    template_id = models.IntegerField(default=0)
    due_amount = models.CharField(max_length=500,null=True)
    current_disposition = models.CharField(max_length=500,null=True)
    calling_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    is_pulled = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateField(null=True, blank=True)
    scheduled_at = models.DateTimeField(default =future_date_and_time, null=True, blank=True)
    name = models.CharField(max_length=500,null=True)
    status = models.CharField(max_length=500,null=True)

   

class DailyReport(models.Model):
    # id = models.AutoField(primary_key=True)
    loan_account_no = models.CharField(max_length=500, null=True, blank=True)
    agency_name  = models.CharField(max_length=500, default="The Medius") 
    product_name = models.CharField(max_length=500, null=True, blank=True)
    due_agmt_no = models.CharField(max_length=500, null=True, blank=True)
    customer_name = models.CharField(max_length=500, null=True, blank=True)
    mobile_number = models.CharField(max_length=50, null=True, blank=True)
    contact_date = models.DateField(null=True, blank=True)
    due_amount = models.CharField(max_length=500, null=True, blank=True)
    disposition = models.CharField(max_length=500, null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    ptp_date = models.DateField(null=True, blank=True)
    ptp_amount = models.CharField(max_length=500, null=True, blank=True)
    next_action = models.CharField(max_length=500, null=True, blank=True)
    payment_mode = models.CharField(max_length=100, null=True, blank=True)
    paid_amount = models.CharField(max_length=500, null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    channel = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(default=datetime.date.today)
    updated_at = models.DateField(null=True, blank=True)
    


class CallingData(models.Model):
    # id = models.AutoField(primary_key=True)
    customer_phone = models.CharField(max_length=20,null=True)
    call_attempt = models.IntegerField(default=0)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True)
    due_amount = models.CharField(max_length=500,null=True)
    current_disposition = models.CharField(max_length=500,null=True)
    calling_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    is_pulled = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    created_at = models.DateField(default=datetime.date.today, null=True)
    updated_at = models.DateField(null=True, blank=True)


class Action(models.Model):
    # id = models.AutoField(primary_key=True)
    customer_phone = models.CharField(max_length=500,null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True)
    due_amount = models.CharField(max_length=500,null=True)
    current_disposition = models.CharField(max_length=500,null=True)
    due_date = models.DateField(null=True, blank=True)
    channel = models.CharField(max_length=200)
    mail = models.EmailField()
    loan_account_no = models.CharField(max_length=500)
    contacted_date = models.DateField()
    contected_time = models.TimeField()
    first_attempt = models.BooleanField(default=True)
    created_at = models.DateField(default=datetime.date.today, null=True)
    updated_at = models.DateField(null=True, blank=True)




class Account(models.Model):
    # account_id = models.AutoField(primary_key=True)
    account_number = models.CharField(max_length=500, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=500, null=True)
    balance = models.CharField(max_length=500, null=True)
    account_created_at = models.DateField(default=datetime.date.today, null=True)

    def __str__(self) :
        return f"{self.id} - {str(self.account_type)}"



class LastTransaction(models.Model): #
    # txn_id = models.AutoField(primary_key=True)
    transaction_number = models.CharField(max_length=500)
    transaction_amount = models.CharField(max_length=500)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self) :
        return f"{self.id} - {str(self.transaction_number)}"


class Loan(models.Model): 
    # loan_id = models.AutoField(primary_key=True)
    loan_account_number = models.CharField(max_length=500,null=True)
    loan_amount = models.CharField(max_length=500,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    agreement_data = models.DateField(null=True)
    lrn = models.CharField(max_length=500,null=True)
    tenor = models.CharField(max_length=500,null=True)
    adv_emi = models.CharField(max_length=500,null=True)
    mob = models.CharField(max_length=500,null=True)
    bkt = models.CharField(max_length=500,null=True)
    emi = models.CharField(max_length=500, null=True)
    demand = models.CharField(max_length=500,null=True)
    receivable = models.CharField(max_length=500, null=True)
    received = models.CharField(max_length=500, null=True)
    overdue = models.CharField(max_length=500, null=True)
    total_charges = models.CharField(max_length=500, null=True)
    total_od = models.CharField(max_length=500, null=True)
    future_princ = models.CharField(max_length=500, null=True)
    pos = models.CharField(max_length=500, null=True)
    amount_financed = models.CharField(max_length=500, null=True)
    ltv = models.CharField(max_length=500,null=True)
    morat_type = models.CharField(max_length=500,null=True)
    status = models.CharField(max_length=500,null=True)
    payment_type = models.CharField(max_length=500,null=True)
    insurance_type = models.CharField(max_length=500,null=True)
    cbd_receivable = models.CharField(max_length=500, null=True)
    cbd_received = models.CharField(max_length=500, null=True)
    cbd_waived = models.CharField(max_length=500, null=True)
    cbc_due = models.CharField(max_length=500, null=True)
    afc_receivable = models.CharField(max_length=500, null=True)
    afc_received = models.CharField(max_length=500, null=True)
    afc_waived = models.CharField(max_length=500, null=True)
    afc_due =  models.CharField(max_length=500, null=True)
    cash_bnc_receivable = models.CharField(max_length=500, null=True)
    cash_bnc_received = models.CharField(max_length=500, null=True)
    cash_bnc_waived = models.CharField(max_length=500, null=True)
    cash_bnc_due = models.CharField(max_length=500, null=True)
    ins_receivable = models.CharField(max_length=500, null=True)
    ins_received = models.CharField(max_length=500, null=True)
    ins_due = models.CharField(max_length=500, null=True)
    clearing_receivable = models.CharField(max_length=500, null=True)
    clearing_received = models.CharField(max_length=500, null=True)
    clearing_due = models.CharField(max_length=500, null=True)
    od_collectable = models.CharField(max_length=500, null=True)
    demand_collectable = models.CharField(max_length=500, null=True)
    future_outstanding = models.CharField(max_length=500, null=True)
    asset_cost = models.CharField(max_length=500, null=True)
    scheme_code = models.CharField(max_length=500,null=True)
    scheme_name = models.CharField(max_length=500,null=True)


    # loan_account_number loan_amount agreement_data lrn tenor adv_emi mob bkt emi demand receivable received overdue total_charges total_od future_princ
    # pos amount_financed ltv morat_type status payment_type insurance_type cbd_receivable cbd_received cbd_waived cbc_due afc_receivable afc_received 
    # afc_waived afc_due cash_bnc_receivable cash_bnc_received cash_bnc_waived cash_bnc_due ins_receivable ins_received ins_due clearing_receivable clearing_received clearing_due 
    # od_collectable demand_collectable future_outstanding asset_cost scheme_code scheme_name

    def __str__(self) :
        return f"{self.id} - {str(self.loan_account_number)}"

class CustomerHomeAddress(models.Model): # pincode landmark address1 address2 address3 city state region zone mobile_number alt_contact_number created_at
    pincode = models.CharField(max_length=500, null=True)
    landmark = models.CharField(max_length=500, null=True)
    address1 = models.TextField(null=True)
    address2 = models.TextField(null=True)
    address3 = models.TextField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    city = models.CharField(max_length=500,null=True)
    state = models.CharField(max_length=500,null=True)
    region = models.CharField(max_length=500,null=True)
    zone = models.CharField(max_length=500,null=True)
    mobile_number = models.CharField(max_length=15, null=True)
    alt_contact_number = models.CharField(max_length=15, null=True)

    def __str__(self) :
        return f"{self.city} - {str(self.pincode)}"

class CustomerOffice(models.Model): # office_pincode office_landmark office_address1 office_address2 office_address3 office_city office_state office_region office_zone office_mobile_number created_at
    office_pincode = models.CharField(max_length=500, null=True)
    office_landmark = models.CharField(max_length=500, null=True)
    office_address1 = models.TextField(null=True)
    office_address2 = models.TextField(null=True)
    office_address3 = models.TextField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    office_city = models.CharField(max_length=500, null=True)
    office_state = models.CharField(max_length=500, null=True)
    office_region = models.CharField(max_length=500, null=True)
    office_zone = models.CharField(max_length=500, null=True)
    office_mobile_number = models.CharField(max_length=500, null=True)

    def __str__(self) :
        return f"{self.office_city} - {str(self.office_pincode)}"


class CustomerGuarantor(models.Model): # guarantor_name gur_address1 gur_address2 gur_address3 gur_city gur_landmark gur_pincode created_at
    guarantor_name = models.CharField(max_length=500, null=True)
    gur_address1 = models.TextField(null=True)
    gur_address2 = models.TextField(null=True)
    gur_address3 = models.TextField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    gur_city = models.CharField(max_length=500, null=True)
    gur_landmark = models.CharField(max_length=500, null=True)
    gur_pincode = models.CharField(max_length=500, null=True)

    def __str__(self) :
        return f"{self.guarantor_name} - {str(self.gur_city)}"

class Source_details(models.Model):
    source_proposal = models.CharField(max_length=500, null=True)
    source_tw_dealer_code = models.CharField(max_length=500, null=True)
    source_tw_dealer_name = models.CharField(max_length=500, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self) :
        return f"{self.source_proposal} - {str(self.source_tw_dealer_name)}"

class EmiDate(models.Model): # disbursal_date last_collection_date first_emi_date last_emi_date agening last_collection_gap_category cheque_bounce cash_bounce score_category 
                             # segment od_movement unmatured_tenor opening_dpd opening_dpd_bracket payment_frequency dpd_del_string closing_dpd closing_dpd_bracket   
    disbursal_date = models.DateField(null=True)
    last_collection_date = models.DateField(null=True)
    first_emi_date = models.DateField(null=True)
    last_emi_date = models.DateField(null=True)
    agening = models.CharField(max_length=500, null=True)
    last_collection_gap_category = models.CharField(max_length=500, null=True)
    cheque_bounce = models.CharField(max_length=500, null=True)
    cash_bounce = models.CharField(max_length=500, null=True)
    score_category = models.CharField(max_length=500, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    segment = models.CharField(max_length=500, null=True)
    od_movement = models.CharField(max_length=500, null=True)
    unmatured_tenor = models.CharField(max_length=500, null=True)
    opening_dpd = models.CharField(max_length=500, null=True)
    current_dpd_bracket = models.CharField(max_length=500, null=True)
    payment_frequency = models.CharField(max_length=500, null=True)
    dpd_del_string = models.CharField(max_length=500, null=True)
    closing_dpd = models.CharField(max_length=500, null=True)
    closing_dpd_bracket = models.CharField(max_length=500, null=True)

    def __str__(self) :
        return f"{self.disbursal_date} - {str(self.last_collection_date)}"



class Risk(models.Model):
    pre_bnc_risk_seg = models.CharField(max_length=500, null=True)
    post_bnc_risk_seg = models.CharField(max_length=500, null=True)
    bounce_prediction = models.CharField(max_length=500, null=True)
    od_prediction = models.CharField(max_length=500, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    repo_risk_flag = models.CharField(max_length=500, null=True)
    expected_loss = models.CharField(max_length=500, null=True)

    def __str__(self) :
        return f"{self.pre_bnc_risk_seg} - {str(self.post_bnc_risk_seg)}"



class CollectionAgent(models.Model):
    asc_code = models.CharField(max_length=500, null=True)
    asc_name = models.CharField(max_length=500, null=True)
    collector_code = models.CharField(max_length=500, null=True)
    collector_name = models.CharField(max_length=500, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sec_name = models.CharField(max_length=500, null=True)
    territory_manager = models.CharField(max_length=500, null=True)

    def __str__(self) :
        return f"{self.asc_code} - {str(self.sec_name)}"


class Product(models.Model):
    portfolio = models.CharField(max_length=500, null=True)
    product_group = models.CharField(max_length=500, null=True)
    business_portfolio = models.CharField(max_length=500, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=500, null=True)
    model = models.CharField(max_length=500, null=True)
    reg_no = models.CharField(max_length=500, null=True)
    chassis_no = models.CharField(max_length=500, null=True)
    eng_no = models.CharField(max_length=500, null=True)

    def __str__(self) :
        return f"{self.product_code} - {str(self.product_group)}"

class Contacts(models.Model):
    Contacts_s3_uri = models.TextField(null=True, blank=True)

class GetContacts(models.Model):
    GetContacts_s3_uri = models.TextField(null=True, blank=True)

class ConversationWati(models.Model):
    Conversation_Wati_s3_uri = models.TextField(null=True, blank=True)

class Conversation_Wati(models.Model):
    conversationId = models.CharField(max_length=100,blank=True, null=True)
    text = models.TextField(default='', blank=True, null=True)
    # From = models.CharField(max_length=20, default='None', null=True)
    # To = models.CharField(max_length=20, default='None', null=True)
    finalText = models.TextField(default='', blank=True, null=True)
    owner = models.CharField(max_length=20, default='True', null=True)
    # owner = models.BooleanField(default=True)
    created = models.CharField(max_length=40, default='None', null=True)
    eventDescription = models.TextField(default='', blank=True, null=True)
    batch_id = models.CharField(max_length=100, default='None', null=True)
    number = models.CharField(max_length=100, default='None', null=True)
    created_at = models.CharField(max_length=100, default='None', null=True)


class BatchAttachment(models.Model):
    file = models.FileField(upload_to='batch_files')

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(BatchAttachment, self).delete(*args,**kwargs)

class Convo_Wati_Acc_Numb(models.Model):
    number = models.CharField(max_length=20)
    conversation = models.TextField()
    From = models.CharField(max_length=20, default='None', null=True)
    To = models.CharField(max_length=20, default='None', null=True)
    created = models.CharField(max_length=40, default='None', null=True)

class Wati_Webhook(models.Model):
    webhook = models.TextField(null=True, blank=True)
    def __str__(self) :
        return "Saved"


# [
#   {
#     "customer_name": "Shivam",
#     "batch_id": 5,
#     "product_name": "Tractor",
#     "product_amount": 151425,
#     "due_days": 180,
#     "risk_status": "High Risk",
#     "last_disposition": "Broken Promise To pay",
#     "assigned_date": "10th Jan 2021",
#     "first_called_date": "11th Jan 2021",
#     "last_disposition_date": "11th Jan 2021"
#   },
#   {
#     "customer_name": "Saurav",
#     "batch_id": 5,
#     "product_name": "Tractor",
#     "product_amount": 155825,
#     "due_days": 160,
#     "risk_status": "High Risk",
#     "last_disposition": "Broken Promise To pay",
#     "assigned_date": "10th Jan 2021",
#     "first_called_date": "11th Jan 2021",
#     "last_disposition_date": "11th Jan 2021"
#   }
# ]
