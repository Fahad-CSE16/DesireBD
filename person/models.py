from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User,AbstractUser
from PIL import Image
from multiselectfield import MultiSelectField
# from main.models import Store
class UserProfile(models.Model):
    GENRE_CHOICES = (
        ('Male', 'MALE'),
        ('Female', 'FEMALE'),
    )
    MARITAL_STATUS_CHOICES = (
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'),
        ('Divorced', 'Divorced'),
        ('Engaged', 'Engaged'),
        ('Separated', 'Separated'),
    )
    CATEGORY=(
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Employee', 'Employee'),
        ('Employeer', 'Employeer'),
    )
    BLOOD_GROUP=(
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        
    )
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birth_date = models.DateField()
    blood_group=models.CharField(max_length=3, choices=BLOOD_GROUP)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    address = models.CharField(max_length=150)
    phone=models.CharField(max_length=13)
    nationality = models.CharField(max_length=30)
    marital_status = models.CharField(max_length=50, choices=MARITAL_STATUS_CHOICES)
    religion = models.CharField(max_length=50)
    biodata=models.TextField()
    profession=models.CharField(max_length=50,choices=CATEGORY,null=True)
    image=models.ImageField(default='default.jpg', upload_to='tuition/images')

    def __str__(self):
        return f'{self.user.username} Profile'
    AUTH_PROFILE_MODULE = 'app.UserProfile'
    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300 :
            output_size =(300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
class SSC(models.Model):
    GROUP = (
        ('Science', 'Science'),
        ('Business_Studies', 'Business_Studies'),
        ('Humanities', 'Humanities'),
        
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ssc')
    group = models.CharField(max_length=100, choices=GROUP)
    institute = models.CharField(max_length=200)
    gpa = models.CharField(max_length=20)
    board=models.CharField(max_length=20)
    passing_year = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save()

class HSC(models.Model):
    GROUP = (
        ('Science', 'Science'),
        ('Business_Studies', 'Business_Studies'),
        ('Humanities', 'Humanities'),

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hsc')
    group = models.CharField(max_length=100, choices=GROUP)
    institute = models.CharField(max_length=200)
    gpa = models.CharField(max_length=20)
    board = models.CharField(max_length=20)
    passing_year = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save()

class AfterHsc(models.Model):
    DEGREE = (
        ('Honours', 'Honours'),
        ('Degree', 'Degree'),
        ('Diploma', 'Diploma'),

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='afterhsc')
    Etype = models.CharField(max_length=100, choices=DEGREE)
    degree=models.CharField(max_length=200)
    institute = models.CharField(max_length=200)
    cgpa = models.CharField(max_length=20)
    passing_year = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save()
class HigherStudies(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='higherstudies')
    masters=models.CharField(max_length=200)
    phd=models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super().save()

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=13,  default="")
    content = models.TextField()
    timeStamp=models.DateTimeField(auto_now_add=True, blank= True)
    def __str__(self):
        return 'message from '+ self.name +' - '+ self.email

class Subject(models.Model):
    name=models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Classes(models.Model):
    name=models.CharField(max_length=150)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    
class SubDistrict(models.Model):
    name = models.CharField(max_length=400)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='subdistrict')

    def save(self, *args, **kwargs):
        super(SubDistrict, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
class TuitionClass(models.Model):
    STATUS = (
        ('Available', 'Available'),
        ('Busy', 'Busy'),
    )
    Choice_style = (
        ('Group_Tuition', 'Group Tuition'),
        ('Private_Tuition', 'Private Tuition'),
    )
    Choice_Place = (
        ('Class_Rooms', 'Class Rooms'),
        ('Coaching_Center', 'Coaching Center'),
        ('Home_Visit', 'Home Visit'),
        ('My_Place', 'My Place'),
    )
    Choice_Approach = (
        ('Online_Help', 'Online Help'),
        ('Phone_Help', 'Phone Help'),
        ('Provide_Hand_Notes', 'Provide Hand_Notes'),
        ('Video_Tutorials', 'Video Tutorials'),
    )
    Choice_Medium = (
        ('Bangla_Medium', 'Bangla Medium'),
        ('English_Medium', 'English Medium'),
        ('Arabic_Medium', 'Arabic Medium'),
        ('Hindi_Medium', 'Hindi Medium'),
        ('Sports_Section', 'Sports Section'),
        ('Singing_Section', 'Singing Section'),
        ('Dance_Section', 'Dance Section'),
        ('Extra Curricular Activities', 'Extra Curricular Activities'),
        ('Language Learning', 'Language Learning'),
        ('Computer Learning', 'Computer Learning'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tuitionclass')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='district')
    preferedPlace=models.ManyToManyField(SubDistrict, related_name='city_set')
    style = MultiSelectField(choices=Choice_style, max_choices=3, max_length=100)
    place = MultiSelectField(choices=Choice_Place,
                             max_choices=3, max_length=100)
    approach = MultiSelectField(choices=Choice_Approach,
                             max_choices=3, max_length=100)
    medium = MultiSelectField(choices=Choice_Medium,
                             max_choices=3, max_length=100)
    subject = models.ManyToManyField(Subject, related_name='subjects')
    level = models.ManyToManyField(Classes, related_name='classes')
    salary = models.CharField(max_length=100)
    days=models.CharField(max_length=100)
    high_education = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS)
    

# class Person(models.Model):
#     name=models.CharField(max_length=100)
#     subject=models.ManyToManyField(Subject, related_name='subject')
#     def __str__(self):
#         return self.name
        
    
    
