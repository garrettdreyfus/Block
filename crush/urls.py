from django.conf.urls import patterns, url

from crush import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about,name='about'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^registration/usernameVal/$', views.usernameVal, name='usernameVal'),
    
    url(r'^userview/$', views.userview, name='userview'),
    url(r'^registration/register/$', views.register, name='register'),
    url(r'^school_profile/$', views.school_profile, name='school_profile'),
    url(r'^school_home/$', views.school_home, name='school_home'),
    url(r'^school_access/$', views.school_access, name='school_access'),
    url(r'^school_profile/addClass/$', views.addClass, name='addClass'),
    url(r'^school_profile/addStudents/$', views.addStudents, name='addStudents'),
    url(r'^school_profile/run_the_sort/$', views.run_the_sort, name='run_the_sort'),
    url(r'^user_access/$', views.user_access, name = 'user_access'),
    url(r'^userview/pref_reg/$', views.pref_reg, name = 'pref_reg'),
<<<<<<< HEAD
    url(r'^school_profile/change_prefs/$', views.change_prefs, name='change_prefs')
=======
    url(r'^school_home/change_prefs/$', views.change_prefs, name='change_prefs')
>>>>>>> parent of daa5f92... AYAYAYYAYAY
)
