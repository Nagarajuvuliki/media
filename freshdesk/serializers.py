from rest_framework import serializers
from .models import FreshDeskTicket, FreshDeskAgent, Converjations
from utils.customSerializers import DynamicFieldsModelSerializer, NestedSerializerField

class FreshDeskTicketSerializers(DynamicFieldsModelSerializer):
    class Meta:
        model = FreshDeskTicket
        fields = '__all__'
        
class FreshDeskAgentSerializers(serializers.ModelSerializer):
    class Meta:
        model = FreshDeskAgent
        fields = '__all__'