from django.db import models
from company.models import Employee
from django.utils.timezone import now

# Create your models here.

class EmployeeAttendance(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    counted_attendance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_in = models.DateTimeField(default=now)
    time_out = models.DateTimeField(default=now)
    type = models.CharField(max_length=16, default='Daily')
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)

    @property
    def work_time(self):
        work = (self.time_out-self.time_in).seconds/60.0
        if work<240:
            pass
        elif work>240 and work<300:
            work = 240.0
        elif work>300 and work<540:
            work = work - 60.0
        elif work > 540:
            work = 480.0
        else:
            work = 0.0
        return work





