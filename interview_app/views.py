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


@api_view(['GET'])
def interviewer_get(request):
    if request.method == 'GET':
        interviwerdetails = Interviewer.objects.all()
        serializer = InterviewerSerializer(interviwerdetails,many=True)
        return Response(serializer.data)
   
@api_view(['POST'])
def interviewer_post(request):
    if request.method =='POST':
        serializer = InterviewerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)   


@api_view(['GET'])
def candidate_get(request):
    if request.method == 'GET':
        candidatedetails = Candidate.objects.all()
        serializer = CandidateSerializer(candidatedetails,many=True)
        return Response(serializer.data)


@api_view(['POST'])
def candidata_post(request):
    if request.method =='POST':
        serializer = CandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK) 


@api_view(['POST'])
def interview_details(request):
    if request.method == 'POST':
        try:
            interviewerName = request.data['interviewerName']
            CandidateName = request.data['CandidateName']
            date = request.data['date']
            interview_time = request.data['interview_time']

            interviwerdetails = Interviewer.objects.get(id = interviewerName)
            iser = InterviewerSerializer(interviwerdetails)

            candidatedetails = Candidate.objects.get(id = CandidateName)
            cser = CandidateSerializer(candidatedetails)

            # interviewer available times
            itf = iser.data['time_from'] 
            itt = iser.data['time_to']

            # interviewer available time
            ctf = cser.data['time_from']
            ctt = cser.data['time_to']

            # checking date availabity 
            if date == cser.data['date']:
                # checking time availabity 
                if itf < interview_time < itt:
                    if ctf < interview_time < ctt:
                        data_dict = {'interviewerName': interviewerName, 'CandidateName': CandidateName,
                                    'date': date, 'interview_time': interview_time}
                        query_dict = QueryDict('', mutable=True)
                        query_dict.update(data_dict)
                        interview_details = Interview_Schedule_Serializer(data=query_dict)
                        if interview_details.is_valid():
                            interview_details.save()
                            data = {"data": interview_details.data}
                            return Response(data, status=status.HTTP_200_OK)
                        else:
                            data = {'status': 400}
                            return Response(data, status=status.HTTP_200_OK)
                    else:
                        return JsonResponse(cser.data['CandidateName']+' is not available in this time.Please select anthoner Time Slot.'+'Select between '+ctf+'-'+ctt,safe=False)
                else:
                    return JsonResponse(iser.data['interviewerName']+' is not available in this time.Please select anthoner Time Slot.'+'Select between '+itf+'-'+itt,safe=False)
                        
            else:
                return JsonResponse(cser.data['CandidateName']+' is not available in this '+date+'.Please select anthoner Candidate.',safe=False)   
        except:
                serializer = Interview_Schedule_Serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data,status=status.HTTP_200_OK)    
            

@api_view(['GET'])
def interview_schedule_get(request):
    if request.method == 'GET':
        interview = Interview_Schedule.objects.all()
        serializer = Interview_Schedule_Serializer(interview,many=True)
        return Response(serializer.data)