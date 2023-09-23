from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from .forms import UserForm, ProjectFilterForm
from .models import User, Student, University, Tags, Project, Comment
from .models import Follow,Feed
from .forms import UserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from .summarizer import summarize_readme
# Create your views here.

def projectDetails(request, pk):
    project = Project.objects.get(pk=pk)
    contributors = project.contributors.all()
    tags = project.tags.all()
    current_user = request.user
    isContributor = False
    for contributor in contributors:
        if current_user == contributor:
            isContributor = True
            break
    comments = Comment.objects.filter(project=project)
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = Student.objects.get(user=current_user)
        comment_obj = Comment(user=user, project=project, comment=comment)
        comment_obj.save()
    
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
    student = Student.objects.get(user=request.user)
    follow = Follow.objects.filter(student=student)
    for i in follow:
        # i is an object of class follow
        feed= Feed.objects.filter(project=i.project).order_by('date_created').reverse()[:1]
        feedlistperproj=[]
        for j in feed:
            # j is an object of class feed with project i
            feedlistperproj.append(j)
        feedlist.append(feedlistperproj)

    context={
        "feed": feedlist
    }
    # Access the values this way #delete after use
    for i in feedlist:
        for j in i:
            print("projname",j.project.name)
            print("message",j.message)

    return render(request,'feed.html', context)
def knowmore(request,pk):
    feedlist=[]
    student = Student.objects.get(user=request.user)
    follow = Follow.objects.filter(student=student)
    for i in follow:
        # i is an object of class follow
        feed= Feed.objects.filter(project=i.project).order_by('date_created').reverse()
        feedlistperproj=[]
        for j in feed:
            # j is an object of class feed with project i
            feedlistperproj.append(j)
        feedlist.append(feedlistperproj)

    context={
        "feed": feedlist
    }
    return render(request,'update.html', context)