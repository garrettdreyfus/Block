from django.conf.urls import patterns, url

from crush import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about,name='about'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^registration/usernameVal/$', views.usernameVal, name='usernameVal'),
    
    url(r'^userview/$', views.userview, name='userview'),
    url(r'^register/$', views.register, name='register'),
    url(r'^school_profile/$', views.school_profile, name='school_profile'),
    url(r'^school_profile/$', views.school_profile, name='school_profile'),
    url(r'^school_profile/addClass/$', views.addClass, name='addClass'),
    url(r'^school_profile/addStudents/$', views.addStudents, name='addStudents'),
    url(r'^school_profile/log_in_master/$', views.log_in_master, name='log_in_master'),
    url(r'^school_profile/run_the_sort/$', views.run_the_sort, name='run_the_sort'),
    url(r'^user_access/$', views.user_access, name = 'user_access'),
    url(r'^userview/pref_reg/$', views.pref_reg, name = 'pref_reg'),
    url(r'^school_profile/change_prefs/$', views.change_prefs, name='change_prefs'),
    url(r'^school_profile/deleted/$', views.deleted, name='deleted'),
    url(r'^school_profile/Publish/$', views.Publish, name='Publish'),
    url(r'^school_profile/edit_class/$', views.edit_class, name='edit_class'),
    url(r'^school_profile/logout_view/$', views.logout_view, name='logout_view'),
    url(r'^school_profile/logout_view/$', views.logout_view, name='logout_view'),
    url(r'^userview/logout_view/$', views.logout_view, name='logout_view'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^school_profile/deadline/$', views.deadline, name='deadline'),
)
