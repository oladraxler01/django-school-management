from django.contrib import admin
from django.urls import path, include
from student import views
from django.conf import settings 
from django.conf.urls.static import static
from student import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('students.html', views.student_list, name='student_list'),
    path('add-teacher.html', views.add_teacher, name='add_teacher'),  # ← ADD THIS
    path('', include('student.urls')),  # Keep this too
    path('', include('home_auth.urls')),
    path('dashboard.html',views.student_dashboard, name='dashboard'),
    path('admin-dashboard.html', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard.html', views.teacher_dashboard, name='teacher_dashboard'),
    path('notification/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read' ),
    path('notification/clear-all', views.clear_all_notification, name= "clear_all_notification")


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    

