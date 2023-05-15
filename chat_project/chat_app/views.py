from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .serializers import UserSerializer
from django.contrib.auth import authenticate,login
from .models import *
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from .signup_form import SignupForm
User=get_user_model()
def connected(request):
    f_person = request.session['user_id']
    first_person = ChatUser.objects.get(id=f_person)
    connection_id = request.GET.get('connection')
    connection = get_object_or_404(Connection, id=connection_id)
    messages = Message.objects.filter(connection=connection)
    return render(request, 'chat_app/connection_created.html',{
        'first_person': first_person, 
        'user2': connection.user2.full_name,
        'messages': messages
    })
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            interests=form.cleaned_data['interests']
            ar=[]
            for x in interests:
                intrst = Interest.objects.create(name=x)
                ar.append(x)
                
            user.save()
            user.interests.add(*ar)
            user.save()
            form.save()
            return render(request, 'chat_app/login.html')
    else:
        form = SignupForm()
    return render(request, 'chat_app/signup.html', {'form': form})

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
  
    
 
