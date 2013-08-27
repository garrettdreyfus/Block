from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
#AUTH_PROFILE_MODULE = 'System.User_profile'
app_label = 'crush'

class SchoolProfile(models.Model):
    school_profile = models.OneToOneField(User,related_name='school_profile')
    Zip_code = models.CharField(max_length=9,null=True)
    def _unicode_(self):
		return (self.profile.username)
class Classes(models.Model):
    School = models.ForeignKey(SchoolProfile, related_name="school", null=True)
    Class_Name= models.CharField(max_length=100, null=False)
    Class_Description= models.CharField(max_length=1000, null=True)
    Max_Occupancy = models.IntegerField(max_length=300)
    Teacher = models.CharField(max_length=20)
    def _unicode_(self):
        return (self.Class_Name)
class User_profile(models.Model):
    user_profile = models.OneToOneField(User,related_name='user_profile')
    School = models.ForeignKey(SchoolProfile, related_name="School", null=True)
    Class_chosen = models.OneToOneField('Preference', related_name="class_chosen", null=True, on_delete=models.SET_NULL)
    Locked = models.BooleanField( default=False)
    def _unicode_(self):
        return (self.profile.username)
        
class Preference(models.Model):
    student = models.ForeignKey(User_profile, related_name="student",on_delete=models.SET_NULL,null=True)
    rank = models.IntegerField(max_length = 1000)
    Class = models.ForeignKey(Classes, related_name="class",on_delete=models.SET_NULL,null=True)
    def __str__(self):  # Python 3: def __str__(self):
        return self.Class.Class_Name
    
