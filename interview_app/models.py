from django.db import models

# Create your models here.

class Interviewer(models.Model):
    interviewerName = models.CharField(max_length=20)
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()

    def __str__(self):
        return self.interviewerName

class Candidate(models.Model):
    CandidateName = models.CharField(max_length=20)
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()

    def __str__(self):
        return self.CandidateName

class Interview_Schedule(models.Model):
    interviewerName = models.ForeignKey(Interviewer,on_delete=models.CASCADE)
    CandidateName = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    date = models.DateField()
    interview_time = models.TimeField()


