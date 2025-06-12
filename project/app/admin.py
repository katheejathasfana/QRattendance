from django.contrib import admin
from . models import Student, Attendance
# Register your models here.
admin.site.register(Student)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'entry_time', 'exit_time']
admin.site.register(Attendance, AttendanceAdmin)
