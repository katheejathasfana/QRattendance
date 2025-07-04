from django.utils import timezone
from io import BytesIO
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout as django_logout
import  qrcode
from django.http import HttpResponse,  JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
# from django.template.loader import render_to_string
from weasyprint import HTML

def admin_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username,password=password)
        if user is not None and user.is_superuser:
            login(request,user)
            return redirect(dashboard)
        else:
            return redirect('login')
    return render(request, 'login.html')

def attendance_today(request):
    today=timezone.now().date()
    attendance_today=Attendance.objects.filter(date=today)
    print(attendance_today)
    return render(request, 'attendance.html', locals())

@login_required    
def dashboard(request):
    today=timezone.now().date()
    start_of_week=today-timedelta(days=today.weekday())
    end_of_week=start_of_week+timedelta(days=6)
    attendances=Attendance.objects.filter(date__range=(start_of_week,end_of_week))
    return render(request, 'dashboard.html', locals())


@login_required
def generate_qr(request):
    qr=qrcode.make('https://asfana.pythonanywhere.com/scan')
    buffer=BytesIO()
    qr.save(buffer,format="PNG")
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='image/PNG')
    response['Content-Disposition'] = 'attachment; filename="qrcode.jpeg"'
    return response

@login_required
def scan_QR(request):
    if request.method=='POST':
        name=request.POST.get("name")
        student=get_object_or_404(Student,name__iexact=name)
        now=timezone.localtime(timezone.now())
        date=now.today()
        attendance, created=Attendance.objects.get_or_create(
            student=student,
            date=date,
            defaults={'entry_time':now}
            )
        if not created:
            attendance.exit_time=now
            attendance.save()
            messages.success(request,'exit  time updated' )
            return redirect('attendance')
        
        messages.success(request,'entry time updated',student.id)
        return redirect('attendance')
            
    return render(request, 'form.html')

@login_required
def add_student(request):
    if request.method=='POST':
        name=request.POST.get('name')
        student_id=request.POST.get('id')
        course=request.POST.get('course')
        join_date=request.POST.get('join_date')
        if not name or not student_id or not join_date or not course:
            messages.error(request, 'all fields are required!')
            return redirect('students')

        student = Student.objects.filter(Q(name__iexact=name) | Q(student_id__iexact=student_id)).exists()
        if not student:
            student=Student.objects.create(student_id=student_id.capitalize(), name=name.capitalize(), course=course, join_date=join_date)
            messages.success(request, f'student {name} added successfully')
            return redirect('students')
        else:
            messages.error(request, 'student with that name already exists')
            return redirect('students')
        
@login_required     
def edit_student(request,id):
    student=get_object_or_404(Student, id=id)
    return render(request, 'edit_student.html',locals())

@login_required
def update_student(request, id):
    student=get_object_or_404(Student, id=id)
    if request.method=='POST':
        student.name=request.POST.get('name')    
        student.student_id=request.POST.get('student_id')   
        student.course=request.POST.get('course')   
        student.join_date=request.POST.get('join_date')   
        student.save()
    return redirect('student_details', id=id)   


@login_required
def students(request) :
    students=Student.objects.all()
    courses=Student.course_choices
    return render(request, 'students.html',locals())  

import calendar
@login_required
def student_details(request,id):
    student=get_object_or_404(Student,id=id)
    months=list(calendar.month_name)
    date=datetime.today()
    month=date.strftime('%B')
    monthly_hour=student.get_monthly_hours(date.month, date.year)
    print(monthly_hour)

    selected_month=request.GET.get('month')
    # selected_year=int(request.GET.get('year'))
    if selected_month and selected_month in months:
        month_number=months.index(selected_month)
        attendance=Attendance.objects.filter(student=student, 
                                         date__month=month_number)
        monthly_hour=student.get_monthly_hours(month_number,date.year)
        month=selected_month
    else:
        attendance=Attendance.objects.filter(student=student)
        print(attendance)
    
    return render(request, 'student_details.html', locals())


def search_student(request):
    q=request.GET.get('q','')
    students=Student.objects.filter(name__icontains=q).values('id', 'name')[:10]
    return JsonResponse(list(students), safe=False)


@login_required
def logout(request):
    django_logout(request)
    return redirect('login')


from django.template.loader import render_to_string
def dowload_attendance(request):
    today=timezone.now().date()
    
    attendance_today=Attendance.objects.filter(date=today)
    string_html=render_to_string('download.html', locals())

    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename=attendance_{today}.pdf'
    HTML(string=string_html, base_url=request.build_absolute_uri()).write_pdf(response)
    print(string_html)
    return response

def download_attendance_by_choose(requset):
    pass




    
