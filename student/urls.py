from django.contrib import admin
from django.urls import path, include
from student import views

urlpatterns = [
    path('students.html', views.student_list, name='student_list'), 
    path('student-details/<slug:slug>/', views.view_student, name='view_student'),
    path('add-student.html', views.add_student, name='add_student'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<str:slug>/',views.delete_student,name='delete_student'),


    path('teachers.html', views.teacher_list, name='teacher_list'),
    path('add-teacher.html', views.add_teacher, name='add_teacher'),
    path('edit-teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'), 
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('teacher-details/<int:teacher_id>/', views.view_teacher, name='view_teacher'),
    path('teacher/update-profile/', views.teacher_update_profile, name='teacher_update_profile'),
    ]
 