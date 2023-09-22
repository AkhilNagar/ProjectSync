from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class University(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    name= models.CharField(max_length=300,default=None)
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    college = models.OneToOneField(University,on_delete=models.CASCADE,default=None)
    major = models.CharField(max_length=300,default=None)
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
    summary = models.TextField(default=None)
    url = models.CharField(max_length=300,default=None)
    tags= models.ManyToManyField(Tags,default=None,blank=True)
    def __str__(self):
        return self.name



class Feed(models.Model):
    project = models.OneToOneField(Project,on_delete=models.CASCADE,default=None)
    message= models.TextField(default=None)
    date_created= models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user= models.OneToOneField(Student,on_delete=models.CASCADE,default=None)
    project = models.OneToOneField(Project,on_delete=models.CASCADE,default=None)
    comment= models.TextField(default=None)