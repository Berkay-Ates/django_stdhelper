from rest_framework import serializers
from .models import Users, Lessons

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name','surname','mail','meal_notify','std_id','is_active']
        

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['lessons_name','class_room','lesson_hour','end_date','user','lesson_id']
        
        
        
        