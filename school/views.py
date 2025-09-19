
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Notification



# Create your views here.

def index(request):
    return render(request , 'authentication/login.html')


def student_details(request):
    return render(request, 'students/student-details.html')

def teacher_dashboard(request):
    return render(request, 'teachers/teacher-dashboard.html')


def student_details(request):
    return render(request, 'students/student-details.html')

def teacher_dashboard(request):
    return render(request, 'teachers/teacher-dashboard.html')

def student_dashboard(request):
    return render(request, 'students/student-dashboard.html')

def view_student(request):
    return render(request, 'student-details.html')

def dashboard(request):
   return render(request, 'students/student-dashboard.html')


