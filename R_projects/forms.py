from django import forms
from .fields import GroupedModelChoiceField
from .models import Research_group, User, Project, Research_area, User_Project

class User_form(forms.ModelForm):
    r_group = GroupedModelChoiceField(queryset=Research_group.objects.exclude(institution = None), choices_groupby='institution')
    
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 
        'first_last_name', 'second_last_name', 'email', 'telephone', 'r_group')



class DateInput(forms.DateInput):
    input_type = 'date'


class Project_form(forms.ModelForm):
    area = GroupedModelChoiceField(queryset=Research_area.objects.exclude(group = None), choices_groupby='group')
    terms = forms.BooleanField(label='Accept terms and conditions')
    director = GroupedModelChoiceField(queryset=User.objects.exclude(director = False), choices_groupby='r_group')

    class Meta:
        model = Project
        fields = ('project_name', 'description', 'requirements', 'director', 'start_date',
         'end_date', 'project_type', 'area', 'accounts', 'cost', 'financing', 'terms')
        
        widgets = {
            'description': forms.Textarea(attrs={'rows':10, 'cols':15, 'style': 'height: 6em; resize:none;'}),
            'requirements': forms.Textarea(attrs={'rows':10, 'cols':15, 'style': 'height: 6em; resize:none;'}),
            'start_date': DateInput(attrs={'type': 'date', 'disabled': True}),
            'end_date': DateInput(attrs={'type': 'date', 'disabled': True}),
            'cost': forms.TextInput(attrs={'disabled': True}),
            'financing': forms.NumberInput(attrs={'disabled': True}),
            'terms': forms.CheckboxInput(),
        }


class Relation_project_user(forms.ModelForm):
    project = GroupedModelChoiceField(queryset=Project.objects.exclude(director = None), choices_groupby='director.r_group')

    class Meta:
        model = User_Project
        fields = ('project', 'token')


class Add_users_form(forms.ModelForm):
    user = GroupedModelChoiceField(queryset=User.objects.exclude(director=True), choices_groupby='r_group')
    project = GroupedModelChoiceField(queryset=Project.objects.exclude(director = None), choices_groupby='director.r_group')
    token = forms.CharField(max_length=30)

    class Meta:
        model = User_Project
        fields = ('user', 'project', 'token')
