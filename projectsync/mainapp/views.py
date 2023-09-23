from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from .forms import UserForm, ProjectFilterForm
from django.db.models import DateTimeField
from .models import User, Student, University, Tags, Project, Comment, Follow, Feed
from .forms import UserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
#from .summarizer import summarize_readme
from .summarizer import summarize_readme
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def projectDetails(request, pk):
    project = Project.objects.get(pk=pk)
    contributors = project.contributors.all()
    tags = project.tags.all()
    current_user = request.user
    print(type(current_user))
    isContributor = False
    for contributor in contributors:
        print(type(contributor))
        if current_user == contributor.user:
            isContributor = True
            print(1)
            break
    print(isContributor)
    comments = Comment.objects.filter(project=project)
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = Student.objects.get(user=current_user)
        comment_obj = Comment(user=user, project=project, comment=comment)
        comment_obj.save()
    
    return render(request, 'projectDetails.html', {'project' : project, 'contributors': contributors, 'tags': tags, 'comments': comments, 'current_user': current_user, 'isContributor': isContributor})
    
def create_announcement(request, project_id):
    project = Project.objects.get(pk=project_id)
    contributors = project.contributors.all()
    tags = project.tags.all()
    current_user = request.user
    isContributor = True
    comments = Comment.objects.filter(project=project)
    if request.method == 'POST':
        message = request.POST.get('announcement_message')
        if message:
            Feed.objects.create(project=project, message=message)
            return redirect('projectDetails', pk = project_id)
        
    return render(request, 'projectDetails.html', {'project' : project, 'contributors': contributors, 'tags': tags, 'comments': comments, 'current_user': current_user, 'isContributor': isContributor})

def studentprofile(request):
    
    if not request.user.is_authenticated:
        return render(request, 'login_required.html')
    # Get the current user's student profile
    current_user = request.user
    student_profile = Student.objects.filter(user=current_user).count()
    if student_profile!=0:
        student_profile = Student.objects.get(user=current_user)
        student_name = student_profile.user.username
        college=student_profile.college
        projects = Project.objects.filter(contributors=student_profile)
        return render(request, 'studentprofile.html', {'student_name': student_name, 'projects': projects,'college':college})
    elif University.objects.filter(user=current_user).count() !=0:
        univ_profile = University.objects.get(user=current_user)
        univ_name = univ_profile.name
        projects = Project.objects.filter(name=univ_name)
        return render(request, 'studentprofile.html', {'student_name': univ_name, 'projects': projects,'college':univ_name})


    #return render(request, 'studentprofile.html', {'student_name': student_name, 'projects': projects,'college':college})

def user_login(request):
    isUniv=False
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
                    
                    if Student.objects.filter(user=user).exists():
                        return render(request,'home.html',{"isUniv":isUniv})
                    else:
                        isUniv=True
                        return render(request,'home.html',{"isUniv":isUniv})
                            
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
    return render(request,'home.html',{"isUniv":False})

def explore(request):
    form = ProjectFilterForm(request.GET)
    projects = Project.objects.filter(is_approved=True)

    if form.is_valid():
        tag = form.cleaned_data['tag']
        search = form.cleaned_data['search']

        if tag:
            projects = projects.filter(tags=tag)

        if search:
            projects = projects.filter(name__icontains=search)

    context = {
        'form': form,
        'filteredProjects': projects,
        'tags': Tags.objects.all(),
    }

    return render(request, 'exploreProjects.html', context)    

def filtered_projects(projects, search_query, selected_tag):
    filtered_projects = []
    for project in projects:
        if project.is_approved:
            if project.name.lower().contains(search_query.lower()) or (selected_tag is project.tags.filter(name=selected_tag).exists()):
                filtered_projects.append(project)
    return filtered_projects
        
# This will be replaced once the upload projects button is created
def uploadProjects(request):
    if request.method=='POST':
        # Fetch Details from HTML
        title = request.POST['project_title']
        project_summary = request.POST['project_summary']
        uni_name = request.POST['uni_name']
        domain_tags = request.POST.getlist('tags')
        collaborator_list = request.POST.get('collaborator_list')
        github_link = request.POST['github_link']
        
        # Prepare data for DB
        if project_summary=="":
            project_summary = summarize_readme(github_link)
        university = University.objects.get(name=uni_name)
        tags = Tags.objects.filter(name__in=domain_tags)
        collaborator_list = collaborator_list.split(',')
        collaborator_list.append(request.user.email)
        print(collaborator_list)
        contributors = Student.objects.filter(user__email__in=collaborator_list)
        plagiarism_score = 0 # Fetch using API

        # Save data in DB
        project_obj = Project(name=title, univ=university, summary=project_summary, url=github_link, plag_score=plagiarism_score)
        project_obj.save()

        project_obj.tags.set(tags)
        project_obj.contributors.set(contributors)
        
        return redirect('explore')
    else:
        domain_tags = Tags.objects.all()
        universities = University.objects.all()
        students = Student.objects.all()
        student_emails = ','.join([student.user.email for student in students])

        current_student = Student.objects.get(user=request.user)
        current_user_uni = current_student.college.name
        print(current_user_uni)
        return render(request, 'uploadForm.html', {'domain_tags': domain_tags, 'universities': universities, 'student_list': student_emails, 'current_user_uni': current_user_uni})


def univhome(request):

    if not request.user.is_authenticated:
        return render(request, 'login_required.html')
    user= User.objects.get(username=request.user.get_username())
    univ= University.objects.get(user=user)
    projects= Project.objects.filter(is_approved=False, univ=univ)
    
    if request.method=="POST":
        print(dict(request.POST.items()))
        projname = request.POST.get("projname")
        print(projname)
        proj= Project.objects.get(name=projname)
        if "accept" in request.POST:
            print("Accepted")
            proj.is_approved=True
            proj.save()
        elif "reject" in request.POST:
            print("Rejected")
            proj.delete()
    context={
        "projects":projects,
    }
    return render(request,'univhome.html', context)

def follow(request,pk):
    project = Project.objects.get(pk=pk)
    student = Student.objects.get(user=request.user)
    follow = Follow(student=student, project=project)
    follow.save()
    return redirect('feed.html')

def feed(request):
    #Top 3 feed items
    feedlist=[]
    feed_dict={}
    project_dict={}
    student = Student.objects.get(user=request.user)
    follow = Follow.objects.filter(student=student)
    for i in follow:
        # i is an object of class follow <student,project>
        feed= Feed.objects.filter(project=i.project).order_by('date_created').reverse()[:3]
        #feed is [feed<p1>,feed<p1>,feed<p2>]
        for j in feed:
            # j is an object of class feed with project i
            if j.project not in feed_dict:
                feed_dict[j.project] = []
            feed_dict[j.project].append((j.message,j.date_created))
            project_dict[j.project]=j.project.pk
    context={
        "feed": feed_dict, "project_dict":project_dict
    }
    # Access the values this way #delete after use
    for key,value in feed_dict.items():
        print("Name: ",key," value: ",value)

    return render(request,'feed.html', context)



def updates(request,pk):
    feed_dict={}
    project = Project.objects.get(pk=pk)
    student = Student.objects.get(user=request.user)
    follow = Follow.objects.filter(student=student)
    for i in follow:
        # i is an object of class follow <student,project>
        feed= Feed.objects.filter(project=i.project).order_by('date_created').reverse()
        #feed is [feed<p1>,feed<p1>,feed<p2>]
    context={
        "feed": feed_dict
    }
    # Access the values this way #delete after use
    for key,value in feed_dict.items():
        print("Name: ",key.pk," value: ",value)
    return render(request,'updates.html', {"feed":feed,"project":project})
    return render(request,'update.html', context)

@csrf_exempt
def webhook(request):    
    # Get the payload of the webhook request.
    data = json.loads(request.body.decode('utf-8'))
    webhook_msg = ""
    if 'pusher' in data and 'name' in data['pusher']:
            pusher_name = data['pusher']['name']
            repository_name = data['repository']['name']
            commits_count = len(data['commits'])
            message = f"New commit in the '{repository_name}' repository by {pusher_name}. {commits_count} commit(s) made."
            webhook_msg += message
            print(message)  # You can replace this with any action you want to take when a commit is made.

            # Print commit messages
            commits = data.get("commits", [])
            for commit in commits:
                commit_message = commit.get("message", "")
                print(f"Commit Message: {commit_message}.")
                webhook_msg += f"Commit Message: {commit_message}."
    
    project_obj = Project.objects.filter(url__contains=data['repository']['name'])
    feed_obj = Feed(project=project_obj, message=webhook_msg)
    feed_obj.save()
    return JsonResponse({"message": "Received"})
