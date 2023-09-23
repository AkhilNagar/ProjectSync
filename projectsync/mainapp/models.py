from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db import models

def __str__(self):
    #username=self.user.username
    return self.user.username

class University(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=None)
    name= models.CharField(max_length=300,default=None)
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=None)
    college = models.ForeignKey(University,on_delete=models.CASCADE,default=None)
    #All information regarding the user
    def __str__(self):
        return self.user.username

class Tags(models.Model):
    name = models.CharField(max_length=30,default=None)
    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=300,default=None)
    univ= models.ForeignKey(University, on_delete=models.CASCADE,default=None)
    contributors = models.ManyToManyField(Student,default=None,blank=True)
    summary = models.TextField(default=None)
    url = models.CharField(max_length=300,default=None)
    tags= models.ManyToManyField(Tags,default=None,blank=True)
    plag_score = models.IntegerField(default=None)
    is_approved = models.BooleanField(default=False)
    date_created= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Feed(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,default=None)
    message = models.TextField(default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.project.name

class Comment(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE,default=None)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,default=None)
    comment = models.TextField(default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.project.name

class Follow(models.Model):
    student= models.ForeignKey(Student, on_delete=models.CASCADE,default=None)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,default=None,blank=True)
