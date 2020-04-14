from django.urls import path
from . import views

app_name = 'R_projects'
urlpatterns = [
    path('', views.index, name='index'),
    path('registration_d/', views.User_r, name='registration_d'),
    path('registration_u/', views.User_r, name='registration_u'),
    path('registration_p/', views.Project_r, name='registration_p'),
    path('add_user/', views.Add_user, name='add_user'),
    path('add_user_success/', views.Add_user_success, name='add_user_success'),
    path('user_detail_r/<int:pk>/', views.user_detail_r, name='user_detail_r'),
    path('project_detail_r/<int:pk>/', views.project_detail_r, name='project_detail_r'),
    path('project_lists', views.project_list, name='project_list'),
]