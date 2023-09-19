from django.shortcuts import render
from .models import User,Student,University
from .forms import UserForm
# Create your views here.



def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        #user=User()
        role = request.POST.get('role')
        user_form=UserForm(data=request.POST)
        if user_form.is_valid():
            userc =user_form.save()
            userc.set_password(userc.password)
            userc.save()
        print(username)
        print(email)
    user_form=UserForm()
    return render(request, 'registration/register.html', {'user_form':user_form})
