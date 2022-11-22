from rest_framework import serializers
from .models import *

class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interviewer
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class Interview_Schedule_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Interview_Schedule
        fields = '__all__'



class laterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview_Schedule
        fields = '__all__'