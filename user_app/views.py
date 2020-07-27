from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from datetime import datetime
import requests
import json
from django.db.models.functions import Concat


class UserViewSet(ViewSet):  

    def list(self, request):
        return Response('Welcome to Tagging System')
    
    def post(self, request):
        """
        Add New User
        Only Admin Group will Have permission to add post
        """
        try: 
            # Add New user 
            ins_user = User.objects.create(username=request.data.get('userName'),
                        first_name = request.data.get('firstName'),
                        last_name = request.data.get('lastName'),
                        is_superuser=False,
                        is_staff=False if request.data.get('vchrGroup').upper()!='ADMIN' else True,
                        is_active =True,
                        email='',
                        date_joined=datetime.now()
            )
            ins_user.set_password(request.data.get('userPassword'))
            ins_user.save()
            
            return Response({'status':'sucess','message':'New User Created'})            

        except Exception as e:
            return Response({'status':0,'message':str(e)})



class UserLoginViewSet(ViewSet):


    """
    Used User login
    """
    def list(self, request):
        return Response('Welcome to Tagging System')


    def post(self, request):
        try:      
            vchr_username= request.data['userName']
            vchr_password=request.data['userPassword']
            user = authenticate(request, username=vchr_username, password=vchr_password)
            if user:
                login(request, user)
                token_json = requests.post('http://'+request.get_host()+'/api-token-auth/',{'username':vchr_username,'password':vchr_password})
                token = json.loads(token_json._content.decode("utf-8"))['token']
                str_name=vchr_username.title() if user.is_staff else (user.first_name +' '+ user.last_name).title()
                userdetails={'Name':str_name}
            
                return Response({'status':'success','token':token,'userdetails':userdetails})
            
            return Response({'status':'failed'})

        except Exception as e:
            return Response({'status':0,'message':str(e)})
