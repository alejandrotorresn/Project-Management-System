from django.db import models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Country(models.Model):
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2)

    def __str__(self):
        return self.country_code


class Institution(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    email_domains = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Group_area(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Research_area(models.Model):
    group = models.ForeignKey(Group_area, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name

class Project_type(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(default='')

    def __str__(self):
        return self.name

class Research_group(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=10)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    areas = models.ManyToManyField(Research_area)

    def __str__(self):
        return self.nickname


class User(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    first_last_name = models.CharField(max_length=20)
    second_last_name = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30, default='')
    email = models.EmailField()
    telephone =  models.CharField(max_length=20)
    r_group = models.ForeignKey(Research_group, on_delete=models.CASCADE)
    start_date = models.DateField()
    active = models.BooleanField(default=False)
    
    director = models.BooleanField(default=False)

    def __str__(self):
        return (self.first_name + ' ' + self.first_last_name + ' (' + self.email + ')')


class Project(models.Model):
    project_name = models.CharField(max_length=300)
    description = models.TextField()
    requirements = models.TextField()
    director = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    project_type = models.ForeignKey(Project_type, on_delete=models.CASCADE)
    area = models.ForeignKey(Research_area, on_delete=models.CASCADE)
    cost = models.PositiveIntegerField(default=0)
    financing = IntegerRangeField(min_value=0, max_value=100, default=0)
    accounts = IntegerRangeField(min_value=1, max_value=4)
    terms = models.BooleanField(default=False)
    activated_accounts = models.SmallIntegerField(default=0)
    active = models.BooleanField(default=False)
    token = models.CharField(max_length=30)

    def __str__(self):
        return self.project_name


class User_Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    token = models.CharField(max_length=30)

    def __str__(self):
        name1 = self.user
        name2 = self.project
        name = str(name1) + ' -----> ' + str(name2)
        return (name)