from django.contrib import admin

from student.models import Parent, Student,Teacher


# Register your models here.
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    search_fields = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    list_filter = ('mother_name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'student_class')
    search_fields = ('first_name', 'last_name', 'student_class')
    list_filter =('gender', 'student_class', 'section')
    readonly_fields =('student_image',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'user__email', 'phone', 'department')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'department')
    list_filter = ('department',)