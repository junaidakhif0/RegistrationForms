from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from app.forms import *

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def home(request):

    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registration(request):

    ufo=UserForm()
    pfo=ProfileForm()

    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            #not saved user object
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            #not saved profile object

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()


            send_mail('Registration',
                       "successfully registration is done",
                       'junaidakhif19@gmail.com',
                       [NSUO.email],
                       fail_silently=False
                       )
    
            return HttpResponse('Data is submitted successfully')
        else:
            return HttpResponse('Invalid Data')
    return render (request,'registration.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        print(username)
        password=request.POST['password']
        print(password)
        AUO=authenticate(username=username,password=password)
        #print(AUO)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid password or username')
        

    return render(request,'user_login.html')

            
