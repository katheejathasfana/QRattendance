from django.utils import timezone
from io import BytesIO
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout as django_logout
import  qrcode
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

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


def dashboard(request):
    attendances=Attendance.objects.all()
    return render(request, 'dashboard.html', locals())


@login_required
def generate_qr(request):
    qr=qrcode.make('http://192.168.68.81/scan')
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

            return HttpResponse("<h1>exit  time updated</h1>")   
        
        return HttpResponse("<h1>entry time updated</h1>")  
            
    return render(request, 'form.html')

@login_required
def add_student(request):
    if request.method=='POST':
        name=request.POST.get('name')
        id=request.POST.get('id')
        course=request.POST.get('course')
        join_date=request.POST.get('join_date')
        if not name or not id or not join_date or course:
            messages.error(request, 'all fields are required!')
            return redirect('students')

        student = Student.objects.filter(Q(name__iexact=name) | Q(student_id__iexact=id)).exists()
        if not student:
            student=Student.objects.create(student_id=id.capitalize(), name=name.capitalize(), course=course, join_date=join_date)
            messages.success(request, f'student {name} added successfully')
            return redirect('students')
        else:
            messages.error(request, 'student with that name already exists')
            return redirect('students')
    
@login_required
def students(request) :
    students=Student.objects.all()
    courses=Student.course_choices
    return render(request, 'students.html',locals())  

@login_required
def student_details(request,id):
    student=get_object_or_404(Student,id=id)
    attendance=Attendance.objects.filter(student=student).order_by('-date')
    print(attendance)
    for i in attendance:
        print(i.entry_time)
    return render(request, 'student_details.html', locals())

@login_required
def logout(request):
    django_logout(request)
    return redirect(login)
