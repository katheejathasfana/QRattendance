from django.utils import timezone
from io import BytesIO
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
import  qrcode
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required

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
   
def scan_QR(request):
    if request.method=='POST':
        name=request.POST.get("name")
        student=get_object_or_404(Student,name__iexact=name)
        now=timezone.localtime(timezone.now())
        print(now)
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


def add_student(request):
    if request.method=='POST':
        name=request.POST.get('name')
        student = Student.objects.filter(name=name).exists()
        if not student:
            Student.objects.creatd(name=name)
            return redirect('dashboard')
        
        return redirect('dashboard')

def students(request) :
    students=Student.objects.all()
    return render(request, 'students.html',locals())  
