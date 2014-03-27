from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
# from django.contrib.auth import *
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import *
from System.models import *
from django import forms
from crush.models import *
from django.core.mail import send_mail
from django.contrib import messages
import csv, re, requests
from django.contrib.auth.decorators import login_required
from operator import *
import datetime
import time, string
from django.utils.timezone import utc
# from paste.util import multidict



@login_required
def notSubmited(request):
    usr = request.user
    user = User_profile.objects.get(user_profile=usr)
    school = user.School
    Students = User_profile.objects.filter(status='student')
    all_stu = []
    for student in Students:
        hrandname = []
        if student.Class_chosen_id == None:
            stu_id = student.id
            student2 = User.objects.get(id=stu_id)
            hrandname.append(student2.username)
            hrandname.append(student.Homeroom)
        all_stu.append(hrandname)
    return render(request, 'crush/notsubmitted.html', {'all_stu':all_stu})
@login_required
def deadline(request):
    usr = request.user
    user = User_profile.objects.get(user_profile=usr)
    school = user.School
    deadline = request.POST
    month = int(deadline["month"])
    day = int(deadline["day"])
    year = int(deadline["year"])
    deadline = datetime.datetime(year, month, day, 23, 59)
    school.deadline = deadline
    school.save()
    return HttpResponseRedirect(reverse('crush:school_profile'))

def sorting(usr, Students):
    done_and_sorted = {}
    Preferences={}
    for student in Students:
        Preferences[student.id] = [] 
        for i in Preference.objects.filter(student = student):
            Preferences[student.id].append((i.Class.Class_Name))
    for i in Classes.objects.all():
	    done_and_sorted[i]=[]
    for i in Students: 
        if i.Class_chosen!=None:
            done_and_sorted[i.Class_chosen.Class].append(i)
    return (done_and_sorted,Preferences)
@login_required
def Publish(request):
    usr = request.user
    ## School = SchoolProfile.objects.get(school_profile=usr)
    Students = User_profile.objects.filter(status='student')
    assignments = Preference.objects.all()
    (done_and_sorted, Preferences) = sorting(usr, Students)
    what_class = {}
    gone_through = []
    for c in done_and_sorted.keys():
	    for user in done_and_sorted[c]:
		    what_class[user.id] = c.Class_Name
    with open('publish.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Student', 'Assignment', 'Homeroom', 'Preferences', 'Rank'])
	for i in assignments:
		if i.student_id not in gone_through:
			gone_through.append(i.student_id)
			q = Classes.objects.get(id=i.Class_id)
			if i.student_id != None:
				user = User_profile.objects.get(id=i.student_id)
				better = Preferences[i.student_id]
				rank = better.index(what_class[user.id])
				better = "; ".join(better)
				spamwriter.writerow([user.user_profile, what_class[user.id], user.Homeroom, better, rank+1])
		else:
			continue
    x = requests.post(
        "https://api.mailgun.net/v2/iceblock.mailgun.org/messages",
        auth=("api", "key-99jb9qto5o4cgelo4zg90l9ki1my7d76"),
        files={"attachment": open("publish.csv")},
        data={"from": "Iceblock admin <justin.kaashoek@gmail.com>",
              "to": [usr.email],
              "subject": 'Final class assignments',
              "text":'Your final class assignments are attached'})
    return HttpResponseRedirect(reverse('crush:school_profile'))
def index(request):
	return render(request, 'crush/index.html', {})
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('crush:index'))
def about(request):
	return render(request, 'crush/about.jade')
def registration(request):
	return render(request, 'crush/registration.jade')
def school_home(request):
	return render(request, 'crush/school_home.html')
def register(request):
    SchoolInfo = request.POST
    Schoolname = SchoolInfo["SchoolName"]
    Admin_name = SchoolInfo["username"]
    Password = SchoolInfo["SchoolPassword_Reg"]
    Check_password = SchoolInfo["SchoolPassword2_Reg"]
    Zip_code = SchoolInfo["Zip_Reg"]
    Email = SchoolInfo["Email"]
    if Password != Check_password:
        messages.add_message(request, messages.ERROR, 'Passwords did not match')
        return HttpResponseRedirect(reverse('index'))
    if SchoolProfile.objects.filter(name = Schoolname).count()>0:
        return HttpResponse("School already exists")
    Usr = User.objects.create_user(Admin_name, Email, Password)
    Usr.save()
    School = SchoolProfile(
        name=Schoolname,
        Zip_code = Zip_code,
    )
    School.save()
    s = SchoolProfile.objects.get(name=Schoolname)
    userprofile = User_profile(
        status = 'admin',
        user_profile = Usr,
        School = School,
        )
    userprofile.save()
    username_check = Admin_name
    password_check = Password
    usr = authenticate(username=username_check, password=password_check)
    if usr is not None:
        if usr.is_active:
            login(request, usr)
            return HttpResponseRedirect(reverse('crush:school_profile'))
    return HttpResponseRedirect(reverse('index'))

@login_required
def edit_class(request):
    ClassInfo = request.POST
    usr = request.user
    oldName = ClassInfo["OldName"]
    Description = ClassInfo["description"]
    MO = ClassInfo["MO"]
    teacher = ClassInfo["Teacher"]
    grade = ClassInfo["Grade"]
    Name = ClassInfo["Class_Name"]
    classes = []
    for course in Classes.objects.all():
	    classes.append(course.Class_Name)
    # print classes
    if oldName not in classes:
	    messages.add_message(request, messages.ERROR, 'The class in the old name field is incorrect')
	    return HttpResponseRedirect(reverse('crush:school_profile'))
    #School = SchoolProfile.objects.get(school_profile=usr)
    course = Classes.objects.get(Class_Name=oldName)
    course.Class_Name = Name
    course.Class_Description=Description
    course.Max_Occupancy=MO
    course.Teacher=teacher
    course.Grade=grade
    course.save()
    return HttpResponseRedirect(reverse('crush:school_profile'))

@login_required
def deleted(request):
    ClassInfo = request.POST
    ClassName = ClassInfo["ClassName"]
    classes = Classes.objects.all()
    c = Classes.objects.get(Class_Name=ClassName)
    prefs = Preference.objects.filter(Class_id = c.id)
    for p in prefs:
        p.delete()
    c.delete()
    return HttpResponseRedirect(reverse('crush:school_profile'))


def user_access(request):
    StudentInfo = request.POST
    Username = StudentInfo["Username"]
    Password = StudentInfo["StudentPassword"]
    usr = authenticate(username=Username, password=Password)
    if usr is not None:
        if usr.is_active:
            if Preference.objects.filter(student = request.user):
                messages.add_message(request, messages.ERROR, "You've already submitted your preferences")
                return HttpResponseRedirect(reverse('crush:index'))

            login(request, usr)            
            return HttpResponseRedirect(reverse('crush:userview'))
    else:
        messages.add_message(request, messages.ERROR, 'Your username or password is invalid')
        return HttpResponseRedirect(reverse('crush:index'))
@login_required
def userview(request):
    usr = request.user
    Student = User_profile.objects.get(user_profile=usr)
    School = Student.School
    classes = Classes.objects.all()
    all_classes = []
    for i in classes:
        if str(Student.Grade) in i.Grade:
            all_classes.append(i)
            # filter(School=School).filter(Grade=Student.Grade)
    return render(request, 'crush/userview.html', {'classes':all_classes, 'deadline':School.deadline})

@login_required
def school_profile(request):
    usr = request.user
    
    not_entered = []
    Admin = User_profile.objects.get(user_profile=usr)
    School = Admin.School
    Students = User_profile.objects.filter(status='student',School=School )
    (done_and_sorted, Preferences) = ({},[])
    for i in Classes.objects.all():
    	done_and_sorted[i]=[]
    for i in Students:
        if len(Preference.objects.filter(student=i)) == 0:
            not_entered.append(i)
    if len(Students) == len(not_entered):
        Entered_Fraction = "0/" + str(len(Students))

    Entered_Fraction = str(len(Students)-len(not_entered)) + ' / ' + str(len(Students))
    return render(request, 'crush/school_home.html', {'Students':Students,'Entered_Fraction':Entered_Fraction,'done_and_sorted':done_and_sorted,'Preferences':Preferences, 'deadline':School.deadline})
    
def log_in(request):
    username = request.POST['SchoolName']
    password = request.POST['SchoolPassword']
    user = authenticate(username=username, password=password)
    if user is not None:
        print "DEBUG1:", Preference.objects.filter(student_id = user)
        if user.is_active:
            login(request, user)
            u = User.objects.get(username=username)
            u = User_profile.objects.get(user_profile=u)
            school = u.School
            if u.status == 'admin':
                return HttpResponseRedirect(reverse('crush:school_profile'))
            else:
                if school.deadline != None and datetime.datetime.utcnow().replace(tzinfo=utc) > school.deadline:
                    messages.add_message(request, messages.ERROR, 'Deadline to submit preferences has passed')
                    return HttpResponseRedirect(reverse('crush:index'))
                if len(Preference.objects.filter(student_id = user))==0:
                    messages.add_message(request, messages.ERROR, "You've already entered your Preferences")
                    return HttpResponseRedirect(reverse('crush:index'))
                return HttpResponseRedirect(reverse('crush:userview'))
        else:
            return HttpResponseRedirect(reverse('crush:index'))
    else:
        messages.add_message(request, messages.ERROR, 'Your username or password is invalid')
        return HttpResponseRedirect(reverse('crush:index'))

    username = request.POST['SchoolName']


@login_required
def log_in_master(request):
    username = request.POST['SchoolName']
    password = request.POST['SchoolPassword']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            u = User.objects.get(username=username)
            u = User_profile.objects.get(user_profile=u)
            school = u.School
            if u.status == 'admin':
                return HttpResponseRedirect(reverse('crush:school_profile'))
            else:
                return HttpResponseRedirect(reverse('crush:userview'))
        else:
            return HttpResponseRedirect(reverse('crush:index'))
    else:
        messages.add_message(request, messages.ERROR, 'Your username or password is invalid')
        return HttpResponseRedirect(reverse('crush:index'))

@login_required
def addMultipleClasses(request):
    csvfile = request.FILES['spreadsheet']
    csvfile = csvfile.read()
    usr = request.user
    user = User_profile.objects.get(user_profile=usr)
    school = user.School
    rowsp= csvfile.split('\r')
    rows=[]
    for row in rowsp[1:]:
        row = row.split('\t')
        if len(row)==0:
            return HttpResponseRedirect(reverse('crush:school_profile'))
        if len(row) < 5:
            messages.add_message(request, messages.ERROR, "Row %s doesn't have enough fields" % row)
            return HttpResponseRedirect(reverse('crush:school_profile'))
        name = row[0].decode('utf-8', 'ignore')
        try:
            r = Classes.objects.get(Class_Name=name)
            messages.add_message(request, messages.ERROR, "Class %s already exists" % name)
            continue
        except Classes.DoesNotExist:
            teacher = row[1].decode('utf-8', 'ignore')
            capacity = row[4]
            grades = row[3]
            grades = grades.replace('\"', "")
            ngrade = []
            print row
            start = grades[0]
            end = grades[-1]
            description = row[2].decode('utf-8', 'ignore')
            if len(grades) != 1:
                try:
                    s = int(start)
                    e = int(end)
                    for i in range(s, e+1):
                        ngrade.append(i)
                except:
                    messages.add_message(request, messages.ERROR, "Grade info entered incorrecly (%s,%s) for row %s" % (start, end, row))
                    continue
            Class = Classes(
                School=school,
                Class_Name=name,
                Class_Description=description,
                Max_Occupancy=capacity,
                Teacher=teacher,
                Grade=ngrade,    
                )
            try:
                Class.save()
            except:
                messages.add_message(request, messages.ERROR, "Weird characters in row %s" % row)
    return HttpResponseRedirect(reverse('crush:school_profile'))

@login_required
def addSingleClass(request):
    ClassInfo = request.POST
    usr = request.user
    Admin = User_profile.objects.get(user_profile=usr)
    School = Admin.School
    Description = ClassInfo["ClassDescription"]
    Name = ClassInfo["ClassName"]
    try:
        r = Classes.objects.get(Class_Name=Name)
        messages.add_message(request, messages.ERROR, "Class %s already exists" % Name)
        return HttpResponseRedirect(reverse('crush:school_profile'))
    except Classes.DoesNotExist:
        MO = ClassInfo["MO"]
        teacher = ClassInfo["Teacher"]
        grade = ClassInfo["Grade"]
        ngrade = []
        start = grade[0]
        end = grade[-1]
        if len(grade) == 1:
            ngrade.append(int(grade))
        else:
            for i in range(int(start), int(end)+1):
                ngrade.append(i)
        # print ngrade
        Class = Classes(
            School=School,
            Class_Name=Name,
            Class_Description=Description,
            Max_Occupancy=MO,
            Teacher=teacher,
            Grade=ngrade,    
        )
        Class.save()
    return HttpResponseRedirect(reverse('crush:school_profile'))

@login_required
def addStudents(request):
    csvfile = request.FILES['spreadsheet']
    csvfile = csvfile.read()
    usr = request.user
    user = User_profile.objects.get(user_profile=usr)
    school = user.School
    rowsp= csvfile.split('\r')
    # rowsp = rowsp[0].split('\n')
    rows=[]
    ## for i in rowsp:
    ##     rows.append(i.split(','))
    for row in rowsp[1:]:
        row = row.split(',')
        if len(row)==0:
            return HttpResponseRedirect(reverse('crush:school_profile'))
        if len(row) < 6:
            messages.add_message(request, messages.ERROR, "Row %s doesn't have enough fields" % row)
            return HttpResponseRedirect(reverse('crush:school_profile'))
        username = row[1].lower() + row[0].lower()
        username = username.replace(" ", "")
        username = username[0:30]
        print username, len(username)
        if len(User.objects.filter(username= username))==0:
            user = User.objects.create_user(username)
            admin_bol = row[4].lower()
            user.set_password(row[2])
            user.first_name = row[0]
            user.last_name = row[1]
            print row[4]
            if str(row[4]) == 'student':
                print "GOT HERE"
                user.email = ""
            user.save()
            student = User_profile(
                user_profile=user,
                School = school,
                Grade = row[3],
                Homeroom = row[5],
                status = admin_bol
            )
            student.save()
    return HttpResponseRedirect(reverse('crush:school_profile'))
        
@login_required  
def pref_reg(request):
    dataString = request.POST["data"]
    dataString = dataString.split(',')
    p=0
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
    return HttpResponse(status=201)

def sort( preferenceDict,request):
    #preferenceDict is a dict with student objects as keys and 
    # preference objects as values
    #classDict is a Dictionary with Classes as keys and student objects as dicts.
#    school = SchoolProfile.objects.get(school_profile=request.user)
    classes = Classes.objects.all()
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
        for student_2 in new_sort[new_sort.index(student_1):]:
            if student_1.Locked == False and student_2.Locked == False:
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

@login_required
def run_the_sort (request):
    #school = SchoolProfile.objects.get(school_profile = request.user)
    allStudents = User_profile.objects.filter(status='student')
    studentandprefs = {}
    for student in allStudents:
        studentandprefs[student]= Preference.objects.filter(student=student)
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

@login_required
def usernameVal(request):
	if request.method =="POST":
		response_str="true"
		if User.objects.filter(username=request.POST["SchoolName"]).exists():
			response_str="false"
	return HttpResponse("%s" % response_str)
    
@login_required    
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
    return HttpResponse("Success!")
