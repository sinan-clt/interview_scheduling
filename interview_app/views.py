from django.http import QueryDict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from interview_app.serializers import *
# Create your views here.


@api_view(['GET'])
def home(request):
    url = {
        'interviewer_GET':"http://127.0.0.1:8000/interviewer_get",
        'interviewer_POST':"http://127.0.0.1:8000/interviewer_post",
        'Candidate_GET':"http://127.0.0.1:8000/candidate_get",
        'Candidate_POST':"http://127.0.0.1:8000/candidata_post",
        'Interview_Schedule_GET':"http://127.0.0.1:8000/interview_schedule_get",
        'Interview_Schedule_POST':"http://127.0.0.1:8000/interview_details",
    }
    return Response(url)


# fetching regsitered interviewer details
@api_view(['GET'])
def interviewer_get(request):
    if request.method == 'GET':
        interviwerdetails = Interviewer.objects.all()
        serializer = InterviewerSerializer(interviwerdetails,many=True)
        return Response(serializer.data)
   
   
   
# adding interviewer
@api_view(['POST'])
def interviewer_post(request):
    if request.method =='POST':
        serializer = InterviewerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)   


# fetching regsitered candidate details
@api_view(['GET'])
def candidate_get(request):
    if request.method == 'GET':
        candidatedetails = Candidate.objects.all()
        serializer = CandidateSerializer(candidatedetails,many=True)
        return Response(serializer.data)


# adding candidate
@api_view(['POST'])
def candidata_post(request):
    if request.method =='POST':
        serializer = CandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK) 


# checking availability of the interviewer and candidate
@api_view(['POST'])
def checkSlots(request):
    if request.method == 'POST':
        try:
            interviewerName = request.data['interviewerName']
            CandidateName = request.data['CandidateName']
            date = request.data['date']

            interviwerdetails = Interviewer.objects.get(id = interviewerName)
            iser = InterviewerSerializer(interviwerdetails)

            candidatedetails = Candidate.objects.get(id = CandidateName)
            cser = CandidateSerializer(candidatedetails)

            # interviewer available times
            itf = iser.data['time_from'] 
            itt = iser.data['time_to']

            # candidate available times
            ctf = cser.data['time_from'] 
            ctt = cser.data['time_to']
            
            start_dte = itf
            end_dte = itt
            if ctf > itf:
                start_dte = ctf
            if ctt < itt:
                end_dte = ctt
            
            import datetime as dt
            from datetime import timedelta
            start_dt = dt.datetime.strptime(start_dte, '%H:%M:%S')
            end_dt = dt.datetime.strptime(end_dte, '%H:%M:%S')
            diff = (end_dt - start_dt)
            k=int(diff.seconds/(60*60))
            prev_time = start_dt
            time_intervals = []
            while k > 0:
                new_time = prev_time + timedelta(hours=1)
                time_intervals.append((dt.datetime.strftime(prev_time, '%H:%M:%S'),dt.datetime.strftime(new_time, '%H:%M:%S')))
                prev_time = new_time
                k -= 1
            
            # checking date availabity 
            if date == cser.data['date']:
                return JsonResponse(time_intervals, safe=False)            
            else:
                return JsonResponse(cser.data['CandidateName']+' is not available in this '+date+'.Please select anthoner Candidate.',safe=False)   
        except Exception as e:
            serializer = Interview_Schedule_Serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,status=status.HTTP_200_OK)    
        