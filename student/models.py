from django.db import models
from django.utils.text import slugify
import uuid 
import datetime
from django.contrib.auth.models import User
from home_auth.models import CustomUser



# Create your models here.
class Parent(models.Model):
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100)
    father_mobile = models.CharField(max_length=15)
    father_email = models.EmailField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=15)
    mother_occupation = models.CharField(max_length=100)
    mother_email = models.EmailField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()



    def __str__(self) -> str:
        return f"{self.father_name} & {self.mother_name}"
    

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    student_class = models.CharField(max_length=100)
    religion = models.CharField(max_length=50)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    admission_number = models.CharField(max_length=15)
    section = models.TextField(max_length=100)
    student_image = models.ImageField(upload_to='student/', null=True, blank=True)
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}-{self.admission_number}")
        super(Student,self).save(*args,**kwargs)




    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {(self.admission_number)}"


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Change to     first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    date_joined = models.DateField(auto_now_add=True)
    department = models.CharField(max_length=100, blank=True)  # Simple first
    profile_image = models.ImageField(upload_to='teachers/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}-{str(uuid.uuid4())[:8]}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
 

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    number = models.IntegerField()  # Lesson number in sequence
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")  # Calculated field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    students = models.ManyToManyField(Student, through='Attendance')
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def save(self, *args, **kwargs):
        # Calculate duration automatically
        if self.start_time and self.end_time:
            start_dt = datetime.datetime.combine(self.date, self.start_time)
            end_dt = datetime.datetime.combine(self.date, self.end_time)
            self.duration = (end_dt - start_dt).seconds // 60
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.subject.name} - Lesson {self.number} ({self.date})"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['lesson', 'student']
    
    def __str__(self):
        return f"{self.student} - {self.lesson} - {self.status}"
