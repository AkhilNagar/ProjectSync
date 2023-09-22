from django.shortcuts import render,redirect
from .models import CustomUser,Student,University
from .forms import UserForm
# Create your views here.

def projectDetails(request):
    return render(request, 'projectDetails.html')

def login(request):
    if request.method == "POST":
        print("it is a post")
        print(request.POST)
        if "login" in request.POST:
            print("Entered Univ Signup")
        if "univsignup" in request.POST:
            print("Entered Univ Signup")
        if "studentsignup" in request.POST:
            print("Entered Student Signup")
        
    return render(request, 'login.html')

def logout(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        print("REGISTERED")
            # fullname = request.POST.get('username')
            # email = request.POST.get('email')
            # password = request.POST.get('password')
            # #user=User()
            # role = request.POST.get('role')
            # user_form=UserForm(data=request.POST)
            # if user_form.is_valid():
            #     userc =user_form.save()
            #     userc.set_password(userc.password)
            #     userc.save()
            # print(username)
            # print(email)
        
    user_form=UserForm()
    return render(request, 'home.html', {'user_form':user_form})    

def explore(request):
    return render(request, 'exploreProjects.html')
