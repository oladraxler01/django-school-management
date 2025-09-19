from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden 
from home_auth.models import Notification
from django.utils import timezone
from datetime import datetime, time
from django.db.models import Sum, Count, Q

# Add this to student/views.py
def index(request):
    return render(request, 'Home/index.html')

def add_student(request):
    print("VIEW FUNCTION CALLED!") 
    if request.method == 'POST':
        print("Form submitted!")  
        print("Form data:", dict(request.POST))
        print("Files:", dict(request.FILES))
        
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date_of_birth')
            student_class = request.POST.get('student_class')
            religion = request.POST.get('religion')
            joining_date = request.POST.get('joining_date')
            mobile_number = request.POST.get('mobile_number')
            admission_number = request.POST.get('admission_number')
            section = request.POST.get('section')
            student_image = request.FILES.get('student_image')

            # retrieving parent data from the form 
            father_name = request.POST.get('father_name')
            father_occupation = request.POST.get('father_occupation')
            father_mobile = request.POST.get('father_mobile')
            father_email = request.POST.get('father_email') 
            mother_name = request.POST.get('mother_name')
            mother_occupation = request.POST.get('mother_occupation')
            mother_mobile = request.POST.get('mother_mobile')
            mother_email = request.POST.get('mother_email') 
            present_address = request.POST.get('present_address')   
            permanent_address = request.POST.get('permanent_address')

            # Save the student and parent data to the database
            parent = Parent.objects.create(
                father_name=father_name,
                father_occupation=father_occupation,
                father_mobile=father_mobile,
                father_email=father_email,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                mother_mobile=mother_mobile,
                mother_email=mother_email,
                present_address=present_address,
                permanent_address=permanent_address
            )

            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                date_of_birth=date_of_birth,
                student_class=student_class,
                religion=religion,
                joining_date=joining_date,
                mobile_number=mobile_number,
                admission_number=admission_number,
                section=section,
                student_image=student_image,
                parent=parent
            )

            create_notification(request.user,f"Added Student:{student.first_name}{student.last_name}")    

            messages.success(request, 'Student added successfully!')
            return redirect('add_student')
            
            
        except Exception as e:  # ← FIXED INDENTATION (align with try)
            messages.error(request, f'Error saving student: {str(e)}')
            print(f"Error: {e}")
    
    return render(request, 'students/add-student.html')


def create_notification(user, message):
    """Helper function to create notifications"""
    Notification.objects.create(user=user, message=message)


def student_list(request):
    students = Student.objects.select_related('parent').all()
    print(f"Number of students: {students.count()}")
    
    # FIX: Check if user is authenticated before accessing notification_set
    if request.user.is_authenticated:
        unread_notification = request.user.notification_set.filter(is_read=False)
    else:
        unread_notification = []  # Empty list for anonymous users
    
    context = {
        'student_list': students,
        'unread_notification': unread_notification
    }
   
    return render(request, 'students/students.html', context)

def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    parent = student.parent if hasattr(student, 'parent') else None

    context = {
        'student': student,
        'parent': parent
    }

    if request.method == 'POST':
        print("🔄 FORM SUBMITTED")
        print("📦 Form data:", dict(request.POST))
        print("📦 Files:", dict(request.FILES))
        
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date_of_birth')
            student_class = request.POST.get('student_class')
            religion = request.POST.get('religion')
            joining_date = request.POST.get('joining_date')
            mobile_number = request.POST.get('mobile_number')
            admission_number = request.POST.get('admission_number')
            section = request.POST.get('section')
            student_image = request.FILES.get('student_image')

            # DEBUG: PRINT WHAT'S COMING FROM THE FORM
            print(f"📝 Form first_name: '{first_name}'")
            print(f"📝 Form last_name: '{last_name}'")
            print(f"📝 Current student first_name: '{student.first_name}'")
            print(f"📝 Current student last_name: '{student.last_name}'")

            # retrieving parent data from the form 
            parent.father_name = request.POST.get('father_name')
            parent.father_occupation = request.POST.get('father_occupation')
            parent.father_mobile = request.POST.get('father_mobile')
            father_email = request.POST.get('father_email') 
            parent.mother_name = request.POST.get('mother_name')
            parent.mother_occupation = request.POST.get('mother_occupation')
            parent.mother_mobile = request.POST.get('mother_mobile')
            parent.mother_email = request.POST.get('mother_email') 
            parent.present_address = request.POST.get('present_address')   
            parent.permanent_address = request.POST.get('permanent_address')
            parent.save()

            # Update student
            student.first_name = first_name
            student.last_name = last_name
            student.gender = gender
            student.date_of_birth = date_of_birth
            student.student_class = student_class
            student.religion = religion
            student.joining_date = joining_date
            student.mobile_number = mobile_number
            student.admission_number = admission_number
            student.section = section
            if student_image:
                student.student_image = student_image

            # DEBUG: CHECK BEFORE SAVE
            print(f"💾 About to save - new first_name: '{student.first_name}'")
            print(f"💾 About to save - new last_name: '{student.last_name}'")
            
            student.save()
            create_notification(request.user,f"Added Student:{student.first_name}{student.last_name}")

            # DEBUG: VERIFY AFTER SAVE
            refreshed_student = Student.objects.get(id=student_id)
            print(f"✅ After save - first_name: '{refreshed_student.first_name}'")
            print(f"✅ After save - last_name: '{refreshed_student.last_name}'")

            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
            
        except Exception as e:
            print(f"❌ SAVE ERROR: {str(e)}")
            messages.error(request, f'Error saving student: {str(e)}')
            print(f"Error: {e}")

    return render(request, "students/edit-student.html", context)
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

def view_student(request, slug):
    student = get_object_or_404(Student, slug=slug)
    context = {
        'student': student

    }
    return render(request, 'students/student-details.html',context)


# Add these to student/views.py
def teacher_dashboard(request):
    # Get the Teacher object associated with the current user
    try:
        teacher = Teacher.objects.get(user_id=request.user.id)
        # teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        # Handle case where user doesn't have a teacher profile
        messages.error(request, "You don't have a teacher profile.")
        return redirect('index')  # Or show an error page
    
    # Calculate statistics - NOW THIS WILL WORK!
    total_classes = Lesson.objects.filter(teacher=teacher).count()
    completed_classes = Lesson.objects.filter(teacher=teacher, status='completed').count()
    
    # Get unique students across all lessons taught by this teacher
    total_students = Student.objects.filter(
        attendance__lesson__teacher=teacher
    ).distinct().count()
    
    # Count students who were present at least once
    present_students = Student.objects.filter(
        attendance__lesson__teacher=teacher,
        attendance__status='present'
    ).distinct().count()
    
    total_lessons = Lesson.objects.filter(teacher=teacher).count()
    completed_lessons = Lesson.objects.filter(teacher=teacher, status='completed').count()
    
    # Calculate total hours
    completed_hours = Lesson.objects.filter(
        teacher=teacher, 
        status='completed'
    ).aggregate(total=Sum('duration'))['total'] or 0
    completed_hours = completed_hours / 60  # Convert minutes to hours
    
    total_hours = Lesson.objects.filter(
        teacher=teacher
    ).aggregate(total=Sum('duration'))['total'] or 0
    total_hours = total_hours / 60  # Convert minutes to hours
    
    # Progress percentage
    progress_percentage = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0
    
    # Upcoming lessons (next 5 lessons)
    upcoming_lessons = Lesson.objects.filter(
        teacher=teacher, 
        date__gte=timezone.now().date(),
        status='scheduled'
    ).order_by('date', 'start_time')[:5]
    
    # Teaching history (recent 10 completed sessions)
    teaching_history = Lesson.objects.filter(
        teacher=teacher, 
        status='completed'
    ).order_by('-date', '-start_time')[:10]
    
    # Calendar events
    calendar_events = []
    for lesson in Lesson.objects.filter(teacher=teacher, date__gte=timezone.now().date()):
        calendar_events.append({
            'time': lesson.start_time.strftime('%H:%M'),
            'title': f"{lesson.subject.name} - Lesson {lesson.number}",
            'duration': f"{lesson.duration}min",
            'color': 'blue'
        })
    
    context = {
        'completed_classes': completed_classes,
        'total_classes': total_classes,
        'present_students': present_students,
        'total_students': total_students,
        'completed_lessons': completed_lessons,
        'total_lessons': total_lessons,
        'completed_hours': round(completed_hours, 1),
        'total_hours': round(total_hours, 1),
        'progress_percentage': progress_percentage,
        'upcoming_lessons': upcoming_lessons,
        'teaching_history': teaching_history,
        'calendar_events': calendar_events,
    }
    
    return render(request, 'teachers/teacher-dashboard.html', context)


def student_dashboard(request):
    return render(request, 'students/student-dashboard.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def delete_student(request,slug):
    print(f"DELETE function called with slug: {slug}")  # ADD THIS
    print(f"Request method: {request.method}")  # ADD THIS
    
    if request.method =="POST":
        print("POST request received")  # ADD THIS
        student = get_object_or_404(Student,slug=slug)
        print(f"Found student: {student.first_name} {student.last_name}")  # ADD THIS
        student_name =f"{student.first_name}  {student.last_name}"

        #create_notification(request.user,f"Deleted student :{student_name}")

        student.delete()
        print("Student deleted successfully")  # ADD THIS
        return redirect('student_list')
        
    print("Not a POST request")  # ADD THIS
    return HttpResponseForbidden()


# ADD THESE VIEWS

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teachers.html', {'teachers': teachers})

def add_teacher(request):
    if request.method == 'POST':
        # We'll add form processing later
        return redirect('teacher_list')
    return render(request, 'teachers/add-teacher.html')

def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        # We'll add form processing later  
        return redirect('teacher_list')
    return render(request, 'teachers/edit-teacher.html', {'teacher': teacher})

def delete_teacher(request, teacher_id):
    if request.method == 'POST':
        teacher = get_object_or_404(Teacher, id=teacher_id)
        teacher.delete()
        return redirect('teacher_list')
    return HttpResponseForbidden()

def view_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teachers/teacher-details.html', {'teacher': teacher})


def teacher_update_profile(request):
    if request.method == 'POST':
        # Handle password update logic here
        pass
    return redirect('view_teacher', teacher_id=request.user.teacher.id)

def mark_notification_as_read(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()

def clear_all_notification(request):
    if request.method == "POST":
        notification = Notification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()