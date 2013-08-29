from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import *
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import *
from System.models import *
from django import forms
from crush.models import *
from django.core.mail import send_mail
import csv
from operator import *


def index(request):
	return render(request, 'crush/index.jade')
def about(request):
	return render(request, 'crush/about.jade')
def registration(request):
	return render(request, 'crush/registration.jade')
def school_home(request):
	return render(request, 'crush/school_home.jade')
def register(request):
    SchoolInfo = request.POST
    Username = SchoolInfo["SchoolName_Reg"]
    Password = SchoolInfo["SchoolPassword_Reg"]
    Zip_code = SchoolInfo["Zip_Reg"]
    Email = SchoolInfo["Email"]
    if User.objects.filter(username = Username).count()>0:
        return HttpResponse("Your username is not unique! Try another one")

    Usr = User.objects.create_user(Username, Email, Password)
    Usr.save()
    School = SchoolProfile(
        school_profile=Usr,
        Zip_code = Zip_code,
    )
    School.save()
    username_check = Username
    password_check = Password
    usr = authenticate(username=username_check, password=password_check)
    if usr is not None:
        if usr.is_active:
            login(request, usr)
            return HttpResponseRedirect(reverse('crush:school_profile'))
    return HttpResponseRedirect(reverse('crush:index'))

def user_access(request):
    StudentInfo = request.POST
    Username = StudentInfo["Username"]
    Password = StudentInfo["StudentPassword"]
    usr = authenticate(username=Username, password=Password)
    if usr is not None:
        if usr.is_active:
            login(request, usr)
            
            return HttpResponseRedirect(reverse('crush:userview'))
    else:
        return HttpResponse("Password incorrect! <a href=\"\">Go back and try again</a>");

def userview(request):
    usr = request.user
    Student = User_profile.objects.get(user_profile=usr)
    School = Student.School
    classes = Classes.objects.filter(School=School)
    return render(request, 'userview.jade', {'classes':classes})
    
def school_profile(request):
    usr = request.user
    School = SchoolProfile.objects.get(school_profile=usr)
    not_entered = []
    Students = User_profile.objects.filter(School=School)
    done_and_sorted = {}
    Preferences={}
    for student in Students:
        Preferences[student] = [] 
        for i in Preference.objects.filter(student = student):
            Preferences[student].append((i.Class.Class_Name))
    for i in Students:
        if len(Preference.objects.filter(student=i)) == 0:
            not_entered.append(i)
    for i in Classes.objects.filter(School=School): done_and_sorted[i]=[]
    for i in Students: 
        if i.Class_chosen!=None:
            done_and_sorted[i.Class_chosen.Class].append(i)
    Entered_Fraction = str(len(Students)-len(not_entered)) + ' / ' + str(len(Students))
    return render(request, 'school_home.jade', {'School':School,'Students':Students,'Entered_Fraction':Entered_Fraction,'done_and_sorted':done_and_sorted,'Preferences':Preferences})
    
def school_access(request):
    SchoolInfo = request.POST
    Username = SchoolInfo["SchoolName"]
    Password = SchoolInfo["SchoolPassword"]
    username_check = Username
    password_check = Password
    usr = authenticate(username=username_check, password=password_check)
    if usr is not None:
        if usr.is_active:
            login(request, usr)

            return HttpResponseRedirect(reverse('crush:school_profile'))

    else:
        return HttpResponseRedirect(reverse('crush:index'))

def addClass(request):
    ClassInfo = request.POST
    usr = request.user
    School = SchoolProfile.objects.get(school_profile=usr)
    Description = ClassInfo["ClassDescription"]
    Name = ClassInfo["ClassName"]
    MO = ClassInfo["MO"]
    teacher = ClassInfo["Teacher"]
    Class = Classes(
        School=School,
        Class_Name=Name,
        Class_Description=Description,
        Max_Occupancy=MO,
        Teacher=teacher,
        
    )
    Class.save()
    return HttpResponseRedirect(reverse('crush:school_profile'))
def addStudents(request):
    csvfile = request.FILES['spreadsheet']
    csvfile = csvfile.read()
    
    usr = request.user
    school = SchoolProfile.objects.get(school_profile=usr)
    rowsp= csvfile.split('\r')
    rowsp = rowsp[0].split('\n')
    rows=[]
    for i in rowsp:
        rows.append(i.split(','))
    for row in rows:
        if len(row)==0:
             return HttpResponseRedirect(reverse('crush:school_profile'))
             
        username = row[1].lower() + row[0].lower()
        if len(User.objects.filter(username= username))==0:
            user = User.objects.create_user(username)
            user.set_password(row[2])
            user.first_name = row[0]
            user.last_name = row[1] 
            user.save()
            student = User_profile(
                user_profile=user,
                School = school,
            )
            student.save()
    return HttpResponseRedirect(reverse('crush:school_profile'))
        
    return HttpResponseRedirect(reverse('crush:school_profile'))
def pref_reg(request):
    dataString = request.POST["data"]
    dataString = dataString.split(',')
    p=0
    print dataString
    if Preference.objects.filter(student = request.user) != None:
        existing = Preference.objects.filter(student = User_profile.objects.get(user_profile=request.user)).delete()
    for classname in dataString:
        realclass = Classes.objects.filter(Class_Name= classname)
        usr = User_profile.objects.get(user_profile = request.user)
        pref = Preference(
            student = usr,
            rank = p,
            Class = realclass[0],
        )
        pref.save()
        p+=1
    return HttpResponseRedirect(reverse('crush:index'))

def sort( preferenceDict,request):
    #preferenceDict is a dict with student objects as keys and 
    # preference objects as values
    #classDict is a Dictionary with Classes as keys and student objects as dicts.
    school = SchoolProfile.objects.get(school_profile=request.user)
    classes = Classes.objects.filter(School=school)
    classDict = {}
    for i in classes: classDict[i] = []
    #go through preferenceDict and start dumb sort.
    for student in preferenceDict.keys():
        if student.Locked ==False:
            preferences = preferenceDict[student]
            for i in preferences:
                if i.Class.Max_Occupancy> len(classDict[i.Class]):
                    classDict[i.Class].append(student)
                    break
    return classDict
def reverse_it(Dict):
    #makes a dict of keys ->values("lists") to values-> keys
    new_dict = {}
    for i in Dict.keys():
        for j in Dict[i]:
            new_dict[j]=i
    return new_dict

def switch(sort, preferenceDict, request):
    #sorted will be a dictionary with Classes as keys and students as values
    new_sort = []
    for i in sort.values(): new_sort+=i
    reverse_lookup = reverse_it(sort)
    for student_1 in new_sort[:-1]:
        if student_1.Locked == False and student_2.Locked == False:
            for student_2 in new_sort[new_sort.index(student_1):]:
                class_1 = reverse_lookup[student_1]
                class_2 = reverse_lookup[student_2]
                prefs_1 = []
                for i in preferenceDict[student_1]: prefs_1.append(i.Class)
                prefs_2 = []
                for i in preferenceDict[student_2]: prefs_2.append(i.Class)
                if class_1 in prefs_1 and class_1 in prefs_2 and class_2 in prefs_1 and class_2 in prefs_2:
                    current_score = prefs_1.index(class_1) + prefs_2.index(class_2)
                    potential_score = prefs_1.index(class_2) + prefs_2.index(class_1)
                    if potential_score < current_score:
                        sort[class_1].remove(student_1)
                        sort[class_2].remove(student_2)
                        sort[class_1].append(student_2)
                        sort[class_2].append(student_1)
    return sort
def run_the_sort (request):
    
    school = SchoolProfile.objects.get(school_profile = request.user)
    allStudents = User_profile.objects.filter(School=school)
    studentandprefs = {}
    for student in allStudents: studentandprefs[student]= Preference.objects.filter(student=student)
    # gotta sort studentandprefs
    for prefs in studentandprefs.keys():
        studentandprefs[prefs] = sorted( studentandprefs[prefs], key=attrgetter('rank'))
    done_and_sorted = sort(studentandprefs,request)
    for i in range(10):
        done_and_sorted = switch(done_and_sorted, studentandprefs, request)
    for Cl in done_and_sorted.keys():
        for student in done_and_sorted[Cl]:
            pref = Preference.objects.get(student=student,Class=Cl)
            student.Class_chosen = pref
            student.save()
    return HttpResponseRedirect(reverse('crush:school_profile'))
    
    
def usernameVal(request):
	if request.method =="POST":
		response_str="true"
		if User.objects.filter(username=request.POST["SchoolName"]).exists():
			response_str="false"
	return HttpResponse("%s" % response_str)
    
def change_prefs(request):
    new_class = request.POST["new_class"]
    student = request.POST["usr"]
    usr = User_profile.objects.get(user_profile = student )
    preference = Preference.objects.filter(student=usr)
    final_pref = None
    for i in preference:
        if preference.Class.Class_Name== new_class:
            final_pref = i
    
    rank = final_pref.rank
    cl = final_pref.Class
    final_pref.delete()
    p = Preference(
        student = usr,
        rank = rank,
        Class= cl
    )
    p.save()
    usr.Class_chosen = p
    usr.Locked = True
    usr.save()
    return HttpResponse("Success!");
    

