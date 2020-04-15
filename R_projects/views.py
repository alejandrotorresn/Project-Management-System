from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.base_user import BaseUserManager

from datetime import date
import secrets

from .forms import User_form, Project_form, Relation_project_user, Add_users_form
from .models import Institution, Research_group, User, Country, Project, User_Project

from django.http.request import QueryDict

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse



emails = ['email@mail.com']



def index(request):
    return render(request, 'R_projects/index.html')

def username_verification(username, username_aux, cont):
    # Username verification
    for user in User.objects.all():
        if username_aux == user.username:
            cont = cont + 1
            username_aux = username + str(cont)
            username_aux = username_verification(username, username_aux, cont)
    return username_aux


def username_generator(new_u):
    first_n = new_u.first_name.lower()
    middle_n = new_u.middle_name.lower()
    first_l = new_u.first_last_name.lower()
    second_l = new_u.second_last_name.lower()

    if middle_n == '' and second_l == '':
        username = first_n[0] + first_l
    elif middle_n != '' and second_l == '':
        username = first_n[0] + middle_n[0] + first_l
    elif middle_n == '' and second_l != '':
        username = first_n[0] + first_l + second_l[0]
    elif middle_n != '' and second_l != '':
        username = first_n[0] + middle_n[0] + first_l + second_l[0]

    username = username_verification(username, username, 0)
    
    return username


def domain_verification(new_u):
    domain_u =  new_u.email.split('@')[1]  
    flag_domain = 0
    for institution in Institution.objects.all():
        domains_ins = institution.email_domains.split(',')
        for domain_ins in domains_ins:
            if domain_u.strip() == domain_ins.strip():
                flag_domain = 1
    
    return flag_domain


def send_mail(email_to, email_from, email_subject, email_body):
    email_message = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=email_from,
        to=email_to,
    )
    return email_message


def User_r(request):
    r_groups = Research_group.objects.all()
    institutions = Institution.objects.all()

    if request.path == '/R_projects/registration_d/':
        if request.method == "POST":
            form_director = User_form(request.POST, prefix='form_director')

            if form_director.is_valid():
                new_d = form_director.save(commit=False)
                flag_domain = domain_verification(new_d)
                if flag_domain == 0:
                    return render(request, 'R_projects/r_userd.html', {'form_director': form_director, 'warning': 'The email domain is not linked to a registered institution'} )
                for user in User.objects.all():
                    if new_d.email == user.email:
                        return render(request, 'R_projects/r_userd.html', {'form_director': form_director, 'warning': 'The user\'s email already exists'} )
                
                new_d.first_name = new_d.first_name.capitalize()
                new_d.middle_name = new_d.middle_name.capitalize()
                new_d.first_last_name = new_d.first_last_name.capitalize()
                new_d.second_last_name = new_d.second_last_name.capitalize()
                new_d.start_date = date.today()

                new_d.username = username_generator(new_d)
                new_d.password = BaseUserManager().make_random_password(10)

                new_d.director = True

                # Save user
                new_d.save()

                domain = request.get_host()
                email_body = render_to_string(
                    'R_projects/email_content_director.html', {
                        'full_name': new_d.first_name + ' ' + new_d.first_last_name,
                        'email': new_d.email,
                        'r_group': new_d.r_group.name,
                        'url': domain + reverse('R_projects:user_detail_r', kwargs={'pk':new_d.pk}),
                        'url_admin': domain + '/admin/R_projects/user/' + str(new_d.pk)
                    }
                )                
                email_message = send_mail(emails, 'sc3@uis.edu.co', 'Nuevo registro de director de proyecto', email_body)
                email_message.content_subtype = 'html'
                email_message.send()

                return redirect('R_projects:user_detail_r', pk=new_d.pk)
        else:
            form_director = User_form(prefix='form_director')
        return render(request, 'R_projects/r_userd.html', {'form_director': form_director} )
        
    
    elif request.path == '/R_projects/registration_u/':
        if request.method == "POST":
            form_user = User_form(request.POST, prefix='form_user')
            form_user_project = Relation_project_user(request.POST, prefix='form_user_project')

            flag_u = 0
            flag_pu = 0

            if form_user.is_valid():
                new_u = form_user.save(commit=False)
                flag_domain = domain_verification(new_u)
                if flag_domain == 0:
                    return render(request, 'R_projects/r_user.html', {'form_user': form_user, 'form_user_project': form_user_project, 'warning': 'The email domain is not linked to a registered institution'} )
                for user in User.objects.all():
                    if new_u.email == user.email:
                        return render(request, 'R_projects/r_user.html', {'form_user': form_user, 'form_user_project': form_user_project, 'warning': 'The user\'s email already exists'} )
                
                new_u.first_name = new_u.first_name.capitalize()
                new_u.middle_name = new_u.middle_name.capitalize()
                new_u.first_last_name = new_u.first_last_name.capitalize()
                new_u.second_last_name = new_u.second_last_name.capitalize()
                new_u.start_date = date.today()

                new_u.username = username_generator(new_u)
                new_u.password = BaseUserManager().make_random_password(10)

                new_u.director = False

                flag_u = 1

            if form_user_project.is_valid():
                new_pu = form_user_project.save(commit=False)

                token = ''
                for project_s in Project.objects.all():
                    if new_pu.project ==  project_s:
                        token = project_s.token
                        accounts = project_s.accounts
                        activated_accounts = project_s.activated_accounts
                        pk_value = project_s.pk
                        activated = project_s.active
                
                if activated == False:
                    return render(request, 'R_projects/r_user.html', {'form_user': form_user, 'form_user_project': form_user_project, 'warning': 'Project is not activated'} )

                if new_pu.token != token:
                    return render(request, 'R_projects/r_user.html', {'form_user': form_user, 'form_user_project': form_user_project, 'warning': 'Wrong Token'} )
                
                if activated_accounts >= accounts:
                    return render(request, 'R_projects/r_user.html', {'form_user': form_user, 'form_user_project': form_user_project, 'warning': 'Maximum number of accounts exceeded'} )

                
                flag_pu = 1

            if flag_u == 1 and flag_pu == 1:
                # Save user
                new_u.save()
                # Saver manytomany relationship
                new_pu.user = User.objects.get(pk=new_u.pk)
                new_pu.save()
                # update activated_accounts
                project = Project.objects.get(pk=pk_value)
                project.activated_accounts += 1
                project.save(update_fields=['activated_accounts'])

                domain = request.get_host()
                email_body = render_to_string(
                    'R_projects/email_content_user.html', {
                        'full_name': new_u.first_name + ' ' + new_u.first_last_name,
                        'email': new_u.email,
                        'r_group': new_u.r_group.name,
                        'project': new_pu.project.project_name,
                        'url': domain + reverse('R_projects:user_detail_r', kwargs={'pk':new_u.pk}),
                        'url_admin': domain + '/admin/R_projects/user/' + str(new_u.pk)
                    }
                )                
                email_message = send_mail(emails, 'sc3@uis.edu.co', 'Nuevo registro de usuario', email_body)
                email_message.content_subtype = 'html'
                email_message.send()

                return redirect('R_projects:user_detail_r', pk=new_u.pk)
        else:
            form_user = User_form(prefix='form_user')
            form_user_project = Relation_project_user(prefix='form_user_project')
        return render(request, 'R_projects/r_user.html', {'form_user': form_user, 'form_user_project': form_user_project} )

    return render(request, 'R_projects/index.html')


def token_generator():
    token = secrets.token_hex(15)
    for project in Project.objects.all():
        if token == project.token:
            token = token_generator()
    return token


def Project_r(request):

    if request.method == "POST":
        form_project = Project_form(request.POST)
        if form_project.is_valid():            
            new_p = form_project.save(commit=False)

            if new_p.director.active == False:
                return render(request, 'R_projects/r_project.html', {'form_project': form_project, 'warning': 'The research director is not activated'} )
            
            # Name project verification
            for project in Project.objects.all():
                if new_p.project_name == project.project_name:
                    return render(request, 'R_projects/r_project.html', {'form_project': form_project, 'warning': 'Project name already exists'} )

            # start and end date verification
            if new_p.start_date > new_p.end_date :
                return render(request, 'R_projects/r_project.html', {'form_project': form_project, 'warning': 'The start date is later than the end date'} )

            new_p.token = token_generator()
            new_p.save()

            domain = request.get_host()
            email_body = render_to_string(
                'R_projects/email_content_project.html', {
                    'project_name': new_p.project_name,
                    'description': new_p.description,
                    'requirements': new_p.requirements,
                    'research': new_p.director.first_name + ' ' + new_p.director.first_last_name + ' (' + new_p.director.email + ')',
                    'category': new_p.project_type.name,
                    'start_date': new_p.start_date,
                    'end_date': new_p.end_date,
                    'area': new_p.area.name,
                    'accounts': new_p.accounts,
                    'cost': new_p.cost,
                    'percentage': new_p.financing,
                    'url': domain + reverse('R_projects:project_detail_r', kwargs={'pk':new_p.pk}),
                    'url_admin': domain + '/admin/R_projects/project/' + str(new_p.pk)
                }
            )                
            email_message = send_mail(emails, 'sc3@uis.edu.co', 'Nuevo registro de Proyecto', email_body)
            email_message.content_subtype = 'html'
            email_message.send()

            return redirect('R_projects:project_detail_r', pk=new_p.pk)
    else:
        form_project = Project_form()
    return render(request, 'R_projects/r_project.html', {'form_project': form_project})


def Add_user(request):
    if request.method == "POST":
        form_user_project = Add_users_form(request.POST)

        if form_user_project.is_valid():
            new_pu = form_user_project.save(commit=False)

            for user_project in User_Project.objects.all():
                if new_pu.user.pk == user_project.user.pk and new_pu.project.pk == user_project.project.pk:
                    return render(request, 'R_projects/add_user.html', {'form_user_project': form_user_project, 'warning': 'The user is already linked to this project'} )

            token = ''
            for project_s in Project.objects.all():
                if new_pu.project ==  project_s:
                    token = project_s.token
                    accounts = project_s.accounts
                    activated_accounts = project_s.activated_accounts
                    pk_value = project_s.pk
                    activated = project_s.active

            if activated == False:
                return render(request, 'R_projects/add_user.html', {'form_user_project': form_user_project, 'warning': 'Project is not activated'} )

            if new_pu.user.active == False:
                return render(request, 'R_projects/add_user.html', {'form_user_project': form_user_project, 'warning': 'User is not activated, please contact us to sc3@uis.edu.co'} )

            if new_pu.token != token:
                return render(request, 'R_projects/add_user.html', {'form_user_project': form_user_project, 'warning': 'Wrong Token'} )
                
            if activated_accounts >= accounts:
                return render(request, 'R_projects/add_user.html', {'form_user_project': form_user_project, 'warning': 'Maximum number of accounts exceeded'} )

            # Saver manytomany relationship
            new_pu.save()

            # update activated_accounts
            project = Project.objects.get(pk=pk_value)
            project.activated_accounts += 1
            project.save(update_fields=['activated_accounts'])
            return render(request, 'R_projects/add_user_success.html', {'new_pu': new_pu})

    else:
        form_user_project = Add_users_form()
    return render(request, 'R_projects/add_user.html', {'form_user_project': form_user_project})


def Add_user_success(request):
    return render(request, 'R_projects/add_user_success.html')


def user_detail_r(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'R_projects/user_detail_r.html', {'user': user})


def project_detail_r(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'R_projects/project_detail_r.html', {'project': project})


def project_list(request):
    projects = get_list_or_404(Project)
    return render(request, 'R_projects/project_list.html', {'projects': projects})

