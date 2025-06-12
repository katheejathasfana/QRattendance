from django.db import models
from datetime import datetime
from datetime import time
from django.db.models  import Sum
# Create your models here.
class Student(models.Model):

    course_choices=[('Web Development' , 'Web Development'),
                    ('Graphic Designer' , 'Graphic Designer'),
                    ('Digital Marketing', 'Digital Marketing')]
    
    student_id=models.CharField(max_length=20, unique=True)
    name=models.CharField(max_length=30)
    join_date=models.DateField(null=True)
    course=models.CharField(choices=course_choices, max_length=50)

    def __str__(self):
        return self.name
    
    def get_monthly_hours(self, month, year):
        total_hours=Attendance.objects.filter(
            student=self,
            date__month=month,
            date__year=year
        ).aggregate(total= Sum ('daily_hours'))['total']or 0
        return round(total_hours,2)

class Attendance(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    date=models.DateField()
    entry_time=models.TimeField(null=True,  blank=True)
    exit_time=models.TimeField(null=True, blank=True)
    daily_hours=models.CharField(max_length=5, default='0:00')
    total_hours=models.FloatField(default=0)

    class Meta:
        unique_together=('student','date')

    def __str__(self):
        return f'{self.student.name}: {self.date}'
    
    def save(self,*args, **kwargs):
        if self.date and self.entry_time and self.exit_time:
            entry_time = self.entry_time if isinstance(self.entry_time, time) else self.entry_time.time()
            exit_time = self.exit_time if isinstance(self.exit_time, time) else self.exit_time.time()

            entry=datetime.combine(self.date, entry_time)
            exit=datetime.combine(self.date, exit_time)
            duration=exit-entry
            total_minutes=int(duration.total_seconds()//60)
            hours=total_minutes//60
            minutes=total_minutes % 60

            print(duration)
            self.daily_hours=f"{hours}:{minutes:02d}"
        else:
            self.daily_hours="0.00"
        super().save(*args, **kwargs)


   