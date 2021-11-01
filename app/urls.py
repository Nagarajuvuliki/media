from django.urls import path
from django.conf import settings
from app.batchView import BatchView, BatchDownloadView, TriggerChannels
from app.accountView import AccountView
from app.convoHelper import save_conversations_apii,GotConversationByAthena
from app.post_wati import WatiPostContact
from app.management.commands.importbatch import ImportBatchView
from app.getContactsWati import GetContacts,Save_Contacts_S3
from app import views

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response



urlpatterns = [
    path('batch/', BatchView.as_view(), name='batch'),
    path('trigger_channels/', TriggerChannels.as_view(), name='trigger_channels'),
    path('batch_download/', BatchDownloadView.as_view(), name='batch_download'),
    path('account/', AccountView.as_view(), name='account'),
    path('save_convo_api/', save_conversations_apii.as_view(),name='api2'),
    path('get_convo_sql/', GotConversationByAthena.as_view(),name='get_convo_sql'),
    path('wati_contact/', WatiPostContact.as_view(), name='wati_contact'),
    path('wati_contact_list/', GetContacts.as_view(), name='wati_contact_list'),
    path('import_batch/', ImportBatchView.as_view(), name='import_batch'),
    path('save_contact_list_s3/', Save_Contacts_S3.as_view(), name='save_wati_contact_list_s3'),
    path('save_convo_acc_numb/', views.save_conversations_acc_numb, name='save_wati_contact_list_s3'),
    path('convo_api_acc_numb_of_all/', views.conversations_api_acc_numb.as_view(), name='save_wati_contact_list_s3'),
    path('send_wati_msg/', views.send_msg_from_wati),
    path('customer_data/', views.CustomerData.as_view(), name='customer_data'),
    path('wati_webhook/', views.Wati_Webhook_View.as_view(), name='wati_webhook'),
    
]
