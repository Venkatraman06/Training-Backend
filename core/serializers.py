from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Task, Lead, Client, Proposal, ActivityLog, College, Trainer, Training, Student, PersonalStudent

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'whatsapp']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    assigned_to_details = UserSerializer(source='assigned_to', read_only=True)
    
    class Meta:
        model = Lead
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    assigned_employee_details = UserSerializer(source='assigned_employee', read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'

class ProposalSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    
    class Meta:
        model = Proposal
        fields = '__all__'

class ActivityLogSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = '__all__'

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class TrainerSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Trainer
        fields = '__all__'

class TrainingSerializer(serializers.ModelSerializer):
    college_details = CollegeSerializer(source='college', read_only=True)
    trainer_details = UserSerializer(source='trainer', read_only=True)
    
    class Meta:
        model = Training
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    college_details = CollegeSerializer(source='college', read_only=True)
    trainings_details = TrainingSerializer(source='trainings', many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

class PersonalStudentSerializer(serializers.ModelSerializer):
    trainer_details = UserSerializer(source='trainer', read_only=True)
    
    class Meta:
        model = PersonalStudent
        fields = '__all__'
