from django.db import models
from django.contrib.auth.models import User
from person.models import District
from multiselectfield import MultiSelectField
# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering= ['name']
class Language(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering= ['name']
class Profession(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering= ['name']
class State(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering= ['name']
class Sir_name(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering= ['name']
class Height(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering= ['name']
class Weight(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
class Age(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
class Company(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Religion(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering= ['name']
class Education(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering= ['name']

class Occupation(models.Model):
    WORK_FROM = (
        ('Home', 'Home'),
        ('Work Place', 'Work Place'),
    )
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='occupation')
    occupation = models.CharField(max_length=100, default='workless')
    work_location = models.CharField(max_length=100)
    employed_by = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    salary = models.IntegerField()
    work_from = models.CharField(max_length=100, choices=WORK_FROM)

class Family(models.Model):
    FAMILY_TYPE = (
        ('Joint', 'Joint'),
        ('Nuclear', 'Nuclear'),
    )
    FAMILY_STATUS = (
        ('Affluent', 'Affluent'),
        ('Middle Class', 'Middle Class'),
        ('Rich', 'Rich'),
    )
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='family')
    father_name=models.CharField(max_length=100)
    fathers_occupation=models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mothers_occupation=models.CharField(max_length=100)
    no_of_bro_sis = models.IntegerField()
    family_type=models.CharField(max_length=100,choices=FAMILY_TYPE)
    family_status=models.CharField(max_length=100,choices=FAMILY_STATUS)

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    residency_country = models.CharField(max_length=100)
    birth_country = models.CharField(max_length=100)
    grow_up_country = models.CharField(max_length=100)
    present_address=models.CharField(max_length=300)
    permanent_address = models.CharField(max_length=300)

class Personal_Info(models.Model):
    MARITAL_STATUS_CHOICES = (
        ('Married', 'Married'),
        ('Never Married', 'Never Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('Awaiting Divorces', 'Awaiting Divorces'),

    )
    GENRE_CHOICES = (
        ('Male', 'MALE'),
        ('Female', 'FEMALE'),
    )
    DIET = (
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
    )
    BLOOD_GROUP = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_info')
    full_name = models.CharField(max_length=300)
    sir_name = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=50, choices=MARITAL_STATUS_CHOICES)
    phone = models.CharField(max_length=17)
    is_phone_public = models.BooleanField(default=False)
    religion = models.CharField(max_length=100)
    birth_date = models.DateField()
    age=models.CharField(max_length=30, default='')
    highest_degree_of_education=models.CharField(max_length=30, default='')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP)
    gender = models.CharField(max_length=50, choices=GENRE_CHOICES)
    biodata = models.TextField()
    profile_photo = models.ImageField(default='default.jpg', upload_to='metrimony/images')
    mother_tongue = models.CharField(max_length=150)
    languages = models.ManyToManyField(Language)
    diet = models.CharField(max_length=100, choices=DIET)
    do_u_smoke = models.BooleanField(default=False)
    do_u_drink=models.BooleanField(default=False)
    have_child=models.BooleanField(default=False)

class Body(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='body')
    height = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    eye_color = models.CharField(max_length=20)
    hair_color = models.CharField(max_length=20)
    hair_style = models.CharField(max_length=20)
    complexion = models.CharField(max_length=20)
    any_disability = models.BooleanField(default=False)
    body_type = models.CharField(max_length=50)
class Hobby(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hobby')
    hobbies = models.CharField(max_length=200, null=True)
    interest = models.CharField(max_length=200, null=True)
    music = models.CharField(max_length=200, null=True)
    read_books = models.CharField(max_length=200, null=True)
    tv_shows = models.CharField(max_length=200, null=True)
    sports_shows = models.CharField(max_length=200, null=True)
    sports = models.CharField(max_length=200, null=True)
    fav_dress_style = models.CharField(max_length=200, null=True)
    fav_color = models.CharField(max_length=200, null=True)
    know_dancing=models.BooleanField(default=False)
    know_singing=models.BooleanField(default=False)
    

class Expectaion(models.Model):
    MARITAL_STATUS_CHOICES = (
        ('Married', 'Married'),
        ('Never Married', 'Never Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('Awaiting Divorces', 'Awaiting Divorces'),

    )
    DIET = (
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ecpectation')
    min_age=models.CharField(max_length=20)
    max_age=models.CharField(max_length=20)
    min_height=models.CharField(max_length=20)
    max_height = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS_CHOICES)
    with_childern = models.BooleanField(default=False)
    residency_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='expectaion_country')
    religion = models.CharField(max_length=100)
    complexion = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    drinking_havits = models.BooleanField(default=False)
    smoking_havits = models.BooleanField(default=False)
    diet = models.CharField(max_length=100, choices=DIET)


    
