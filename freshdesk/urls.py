from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static
#from agent import views as ag

urlpatterns = [
    #Tickts
    path('viewtickets/', views.view_tickets),
    path('createticket/', views.CreateTikcet.as_view()),
    path('deletemultipletickets/', views.DeleteMultipleTikcets.as_view()),
    path('deleteticket/<int:id>', views.deleteTikcet),
    path('filterticket/', views.filterTicket),
    path('updateTicket/<int:id>', views.UpdateTicket),
    path('save_all_conversations/', views.save_converjation_in_databse),
    
    #WebHook    
    path('webhook/', views.webhook.as_view()),
    
    #Agent
    path('createagent/', views.CreateAgent.as_view()), 
    path('deleteagent/<int:id>', views.deleteAgent),  
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)