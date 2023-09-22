from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from .models import User,Student,University
from .forms import UserForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def projectDetails(request):
    return render(request, 'projectDetails.html')

def user_login(request):
    if request.method == "POST":
        if "login" in request.POST:
            print("Entered Login")
            email = request.POST.get('email')
            password = request.POST.get('password')
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                return render(request, 'login.html')
            else:
                if user.check_password(password):
                    login(request,user)
                    return render(request, 'home.html')
        
        if "univsignup" in request.POST:
            print("Entered Univ Signup")
            # Save in users
            fullname = request.POST.get('fullname')
            university = request.POST.get('univ')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_form=UserForm(data={'username': university,"email":email,"password":password})
            if user_form.is_valid():
                userc=user_form.save()
                userc.set_password(password)
                userc.save()
            # Save in Univ table also
            obj= User.objects.get(username=university)
            adduniv= University(user=obj, name=university)
            adduniv.save()

        if "studentsignup" in request.POST:
            print("Entered Student Signup")
            fullname = request.POST.get('fullname')
            university = request.POST.get('univ')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_form=UserForm(data={'username': fullname,"email":email,"password":password})
            if user_form.is_valid():
                userc=user_form.save()
                userc.set_password(password)
                userc.save()
            
            # Save in student table also
            obj= User.objects.get(username=fullname)
            obj2= University.objects.get(name=university)
            addstudent= Student(user=obj,college=obj2)
            addstudent.save()
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def explore(request):
    return render(request, 'exploreProjects.html')

# This will be replaced once the upload projects button is created
def uploadProjects(request):
    return render(request, 'uploadForm.html')
