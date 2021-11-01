from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import *
from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta





class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.validated_data['user']
        except:
            user = None
        try:
            message = serializer.validated_data['message']
        except:
            message = None
        if user:
            token, created = Token.objects.get_or_create(user=user)
            now = datetime.now().date() 
            if not created and token.created.date() < now - timedelta(days=15):
                token.delete()
                token = Token.objects.create(user=user)
                token.created = now
                token.save()
        else:
            token = None
        return Response({'token': token, 'message':message})



class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = response.data['token']
        msg = response.data['message']
        if token:
            login_data = {
                'token': token.key, 
                'user_id': token.user.user_id, 
                'full_name': token.user.full_name, 
                'email': token.user.email,
                'role': token.user.role
            }

            response = {
                'status': True,
                'message': 'Login success.',
                'data': login_data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            err_response = {
                'status': False,
                'message': msg,
                'data': None
            }
            return Response(err_response, status=status.HTTP_200_OK)






class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            u_obj = serializer.save()
 
            response = {
                'status': True,
                'message': 'User created successfully.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        else:
            err_response = {
                'status': False,
                'message': serializer.errors,
                'data': None
            }
            return Response(err_response, status=status.HTTP_200_OK)

