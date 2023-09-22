from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from .models import User, Student, University, Tags, Project
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
    if request.method=='POST':
        # Fetch Details from HTML
        title = request.POST['project_title']
        project_summary = request.POST['project_summary']
        uni_name = request.POST['uni_name']
        domain_tags = request.POST.getlist('tags')
        collaborator_list = request.POST.getlist('collaborator_list')
        github_link = request.POST['github_link']
        
        # Prepare data for DB
        university = University.objects.get(name=uni_name)
        tags = Tags.objects.filter(name__in=domain_tags)
        contributors = Student.objects.filter(user__email__in=collaborator_list)
        plagiarism_score = 0 # Fetch using API

        # Save data in DB
        project_obj = Project(projectid=1, name=title, univ=university, summary=project_summary, url=github_link, plag_score=plagiarism_score)
        project_obj.save()

        project_obj.tags.set(tags)
        project_obj.contributors.set(contributors)
        
        return redirect('explore')
    else:
        domain_tags = Tags.objects.all()
        universities = University.objects.all()
        students = Student.objects.all()
        student_emails = ','.join([student.user.email for student in students])
        return render(request, 'uploadForm.html', {'domain_tags': domain_tags, 'universities': universities, 'student_list': student_emails})
