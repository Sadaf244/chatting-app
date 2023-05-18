from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .serializers import UserSerializer
from django.contrib.auth import authenticate,login
from datetime import datetime
from .models import *
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import SignupForm
User=get_user_model()
def connected(request):
    f_person = request.session['user_id']
    first_person = ChatUser.objects.get(id=f_person)
    connection_id = request.GET.get('connection')
    connection = get_object_or_404(Connection, id=connection_id)
   
   
    return render(request, 'chat_app/connection_created.html',{
        'first_person': first_person, 
        'user2': connection.user2.full_name,
        'gender':connection.user2.gender,
        'country':connection.user2.country,  
        'connection':connection ,
       
    })
def signup(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        country = request.POST['country']
        password = request.POST['password']
        interests = request.POST.getlist('interests')
        print(interests)
        interest_objects = []
        for interest_name in interests:
            interest_object = Interest.objects.create(name=interest_name)
            interest_objects.append(interest_object)
        user=ChatUser.objects.create(phone=phone,email=email,full_name=full_name,gender=gender,country=country)    
        user.save()
        user.set_password(password)
        user.interests.set(interest_objects)
        user.save()
       
        return redirect('login')
    else:
        
        return render(request, 'chat_app/signup.html')

def login_view(request):
    if request.method == 'POST':
        input_value = request.POST['email_or_phone']
        password = request.POST['password']
        print(request.POST['email_or_phone'])
        print(request.POST['password'])
        user = None
        # Check if input is email or phone number
        if '@' in input_value:
            # If input is an email, query User model by email
            user = User.objects.filter(email=input_value).first()   
            
        else:
            # If input is a phone number, query User model by phone number
            user = User.objects.filter(phone=input_value).first()
        
        haspassword=user.password    
        if user and check_password(password, haspassword):
            
            user.is_active=True   
            success_message = 'Welcome'
            
            context = {
            'user': user.full_name
            }
            # return render(request, 'chat_app/connection_details.html',context )
            request.session['user_id'] = user.id
            user.save()
            return render(request, 'chat_app/toggle_status.html',context)
        else:
            # If user is not found or password is incorrect, show an error message
            error_message = 'Invalid email/phone number or password'
            return render(request, 'chat_app/login.html', {'error_message': error_message})
    else:
        return render(request, 'chat_app/login.html')

from django.http import HttpResponse, JsonResponse
def toggle_online_status(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        user = ChatUser.objects.get(id=user_id)
        user.is_active = not user.is_active
        status = 'Go Online' if user.is_active else 'Go Offline'
        user.save()
        return JsonResponse({'success': True,'status': status})
          
    else:
        return JsonResponse({'success': False})
def connection(request):  
    
    user_id = request.session['user_id']  
    user = ChatUser.objects.get(id=user_id)
    print(user_id)
    if Connection.objects.filter(user1=user,ended_at=None).exists() :
        connection = Connection.objects.get(user1=user, ended_at=None)
        return render(request, 'chat_app/connection_created.html',{
        'first_person': user.full_name, 
        'user2': connection.user2.full_name,
        'gender':connection.user2.gender,
        'country':connection.user2.country,  
        'connection':connection   
    })
    if Connection.objects.filter(user2=user,ended_at=None).exists() :
        connection = Connection.objects.get(user2=user, ended_at=None)
        return render(request, 'chat_app/connection_created.html',{
        'first_person': user.full_name, 
        'user2': connection.user1.full_name,
        'gender':connection.user1.gender,
        'country':connection.user1.country,   
        'connection':connection   
    })
    arr=[]
    for x in user.interests.all():
        y=Interest.objects.get(id=x.id)
        name=y.name 
        arr.append(name)
   
    usr_idd=user.id
    
    # First, try to find another user with the same interests who is online
    user2 = User.objects.filter(is_active=True, interests__name__in=arr).exclude(id=usr_idd).distinct()
    
    context={
        "other_user":user2,
        
    }
    # If no user is found, connect with anyone who is online
    if not user2:
        online_user = User.objects.filter(is_active=True).exclude(id=usr_idd)
         
        return render(request,'chat_app/connection_details.html',{"online_user":online_user})
    # If no online user is found, show an error message
    if not user2:
        return render(request, 'chat_app/no_connection.html')
    return render(request,'chat_app/connection_details.html',context)
     


def connect_establish(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user1 = request.session['user_id']
        user = ChatUser.objects.get(id=user1)
        other_user = get_object_or_404(User, id=user_id)
        connection = Connection.objects.create(user1=user, user2=other_user)
        connection.save()
        context={
            "user1":user.full_name,
            "user2":other_user.full_name,
            "connection":connection.id
        }
        print(context)
        return JsonResponse(context)  
    else:
        return JsonResponse({'success': False})
    
def logout_view(request):
    user_id = request.session['user_id']  
    user = ChatUser.objects.get(id=user_id)
    print(user.id)
    
    connection = request.GET.get('connection')
    print('connection',connection)
       # Get the active connection id from url
    try:
        connection = Connection.objects.get(id=connection)
        connection.ended_at = datetime.now()
        connection.save()    
        user.is_active=False
        user.save()
        # Logout the user
        return redirect('login')
    except Connection.DoesNotExist:
        raise Exception("No Connection id")
    
    
  
    
 
