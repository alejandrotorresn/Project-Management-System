from django.contrib import admin
from . models import Country, Institution, Research_area, Research_group, Project, User, Project_type, Group_area, User_Project

admin.site.register(Country)
admin.site.register(Institution)
admin.site.register(Research_area)
admin.site.register(Research_group)
admin.site.register(Project_type)
admin.site.register(Project)
admin.site.register(User)
admin.site.register(Group_area)
admin.site.register(User_Project)
