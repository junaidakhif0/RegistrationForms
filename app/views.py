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

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)


def forgotpassword(request):
    if request.method=='POST':
        UN=request.POST['un']
        PW=request.POST['pw']

        LUO=User.objects.filter(username=UN)
        if LUO:
            UO=LUO[0]
            UO.set_password(PW)
            UO.save()
            return HttpResponse('password reset is done')
        
        else:
            return HttpResponse('username is not available in DataBase')
    return render(request,'forgotpassword.html')


                    
