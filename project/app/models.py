from django.db import models
from datetime import datetime
from datetime import time
# Create your models here.
class Student(models.Model):

    course_choices=[('Web Development' , 'Web Development'),
                    ('Graphic Designer' , 'Graphic Designer'),
                    ('Digital Marketing', 'Digital Marketing')]
    
    student_id=models.CharField(max_length=20, unique=True)
    name=models.CharField(max_length=30)
    join_date=models.DateField(null=True)
    course=models.CharField(choices=course_choices)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    entry_time=models.TimeField(null=True,  blank=True)
    exit_time=models.TimeField(null=True, blank=True)
    dialy_hours=models.FloatField(default=0)
    total_hours=models.FloatField(default=0)

    class Meta:
        unique_together=('student','date')

    def __str__(self):
        return f'{self.student.name}: {self.date}'
    
    def save(self,*args, **kwargs):
        if self.entry_time and self.exit_time:
            entry_time = self.entry_time if isinstance(self.entry_time, time) else self.entry_time.time()
            exit_time = self.exit_time if isinstance(self.exit_time, time) else self.exit_time.time()

            entry=datetime.combine(self.date, entry_time)
            exit=datetime.combine(self.date, exit_time)
            duration=exit-entry

            print(duration)
            self.dialy_hours=round(duration.total_seconds()/3600,2)
        else:
            self.dialy_hours=0
        super().save(*args, **kwargs)

        

