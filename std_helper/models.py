from uuid import uuid4
from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=255)
    surname= models.CharField(max_length=255)
    mail = models.EmailField(blank=False,unique=True)
    meal_notify = models.BooleanField(default=False)
    std_id = models.UUIDField(primary_key=True,default=uuid4, editable=False, unique=True, db_index=True)  
    is_active = models.BooleanField(default=False)  
    
    def __str__(self):
        return self.name + ' ' + self.surname + ' ' + self.mail
    
    
    
class Lessons(models.Model):
    lesson_id=models.UUIDField(primary_key=True,default=uuid4, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    lessons_name = models.CharField(max_length=255)
    class_room = models.CharField(max_length=255)
    lesson_hour = models.TimeField()
    end_date = models.DateTimeField()
    
    def __str__(self):
        return self.lessons_name + ' ' + self.class_room 
