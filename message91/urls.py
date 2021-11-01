
from django.urls import path
from . import views
urlpatterns = [
    #add messages
    path('add/', views.add),
    path('update/<int:id>/', views.update),
    path('delete/<int:id>/', views.delete),
    
    #send message
    path('send_message/<int:batch_id>/', views.send_message),
    path('get_message_converjations/', views.get_message_converjations),
    path('get_message_converjations_by_batch_id/<int:batch_id>/', views.get_message_converjations_by_batch_id),
    path('get_message_converjations_by_customer_mobile_number/<str:customer_mobile_number>/', views.get_message_converjations_by_customer_mobile_number),
]