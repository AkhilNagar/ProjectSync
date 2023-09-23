from django.contrib import admin
from mainapp.models import Student, University, Project, Feed, Tags, Comment 

admin.site.register(Student)
admin.site.register(University)
admin.site.register(Project)
admin.site.register(Tags)
admin.site.register(Feed)
admin.site.register(Comment)
#admin.site.register(Follow)