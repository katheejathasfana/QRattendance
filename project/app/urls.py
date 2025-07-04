from django.urls import path
from . import views
urlpatterns=[
    path('qrcode', views.generate_qr ,name="qrcode"),
    path('scan',views.scan_QR, name="scan"),
    path('attendance', views.attendance_today, name='attendance'),
    path('',views.admin_login, name="login"),
    path('dashboard',views.dashboard, name='dashboard'),
    path('add_student', views.add_student, name='add_student'),
    path('students',views.students, name='students'),
    path('student_details/<int:id>', views.student_details,  name='student_details'),
    path('logout', views.logout, name='logout'),
    path('edit_student/<int:id>', views.edit_student, name="edit_student"),
    path('update_student/<int:id>', views.update_student, name="update_student"),
    path('search_student', views.search_student, name='search_student'),
    path('download/', views.dowload_attendance, name='download_pdf')
]
