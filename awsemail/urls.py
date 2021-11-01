from django.urls import path, include
from . import views
urlpatterns = [
    path('sendmail/', views.SendEmail.as_view()),
    path('store_file_on_aws/', views.store_file_on_aws),
    
    #path('message91/', include('message91.urls')),
]