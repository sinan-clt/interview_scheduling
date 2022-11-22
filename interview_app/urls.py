from django.urls import path
from interview_app import views

urlpatterns = [
    path('',views.home,name='home'),
    path('interviewer_get',views.interviewer_get,name='interviewer_get'),
    path('interviewer_post',views.interviewer_post,name='interviewer_post'),
    path('candidate_get',views.candidate_get,name='candidate_get'),
    path('candidata_post',views.candidata_post,name='candidata_post'),
    path('interview_details',views.interview_details,name='interview_details'),   
    path('interview_schedule_get',views.interview_schedule_get,name='interview_schedule_get'),

]