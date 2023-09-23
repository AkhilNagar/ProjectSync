from django.contrib import admin
from mainapp.models import Student, University, Project, Feed, Tags, Comment 
from mainapp.models import Follow
admin.site.register(Student)
admin.site.register(University)
admin.site.register(Project)
admin.site.register(Tags)
admin.site.register(Feed)
admin.site.register(Comment)
#admin.site.register(Follow)