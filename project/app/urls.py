from django.urls import path
from . import views
urlpatterns=[
    path('qrcode', views.generate_qr ,name="qrcode"),
    path('scan',views.scan_QR, name="scan"),
    path('',views.admin_login, name="login"),
    path('dashboard',views.dashboard, name='dashboard'),
    path('add_student', views.add_student, name='add_student'),
    path('students',views.students, name='student'),
]
