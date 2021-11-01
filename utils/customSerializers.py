from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):


    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude_fields is not None:
            excluded = set(exclude_fields)
            existing = set(self.fields.keys())
            
            for field_name in excluded:
                try:
                    self.fields.pop(field_name)
                except:
                    pass





class NestedSerializerField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        self.custom_fields = kwargs.pop('custom_fields', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            if self.custom_fields is not None:
                return self.serializer(instance, context=self.context, fields=self.custom_fields).data
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)