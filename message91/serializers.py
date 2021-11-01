from rest_framework import serializers
from .models import Contact, Message,  SaveBatchConversation
from utils.customSerializers import DynamicFieldsModelSerializer, NestedSerializerField

class MessageSerializers(DynamicFieldsModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
