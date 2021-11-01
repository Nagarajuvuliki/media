from rest_framework import serializers
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from account.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token



class EmailBackend(ModelBackend):
    def authenticate(self, request=None, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None



class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user_request = User.objects.get(email=email,isdeleted=False)
            except:
                user_request = None
            if user_request:
                user = EmailBackend().authenticate(email=email, password=password)
                if user:
                    if not user.is_active:
                        attrs['message'] = 'User account is disabled.'
                    else:
                        attrs['user'] = user
                else:
                    attrs['message'] = 'Incorrect password.'
            else:
                attrs['message'] = 'Incorrect email ID.'
        else:
            attrs['message'] = 'Must include "email" and "password".'
            
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'phone', 'password', 'country', 'role', 'image')
        extra_kwargs = {'password': {'write_only': True, 'required': True}, 'email': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

