from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=30)
    join_date=models.DateField()
    course=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    entry_time=models.TimeField(null=True,  blank=True)
    exit_time=models.TimeField(null=True, blank=True)

    class Meta:
        unique_together=('student','date')

    def __str__(self):
        return f'{self.student.name}: {self.date}'