from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import Task, Lead, Client, Proposal, ActivityLog, College, Trainer, Training, Student, PersonalStudent
from .serializers import (
    TaskSerializer, CustomTokenObtainPairSerializer, UserSerializer,
    LeadSerializer, ClientSerializer, ProposalSerializer, ActivityLogSerializer,
    CollegeSerializer, TrainerSerializer, TrainingSerializer, StudentSerializer, PersonalStudentSerializer
)

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'company', 'college', 'contact_person', 'email']
    ordering_fields = ['created_at', 'expected_deal_value', 'priority']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset

    def perform_update(self, serializer):
        old_status = self.get_object().status
        instance = serializer.save()
        if old_status != 'WON' and instance.status == 'WON':
            Client.objects.get_or_create(
                name=instance.name,
                company=instance.company,
                college=instance.college,
                contact_person=instance.contact_person,
                phone=instance.phone,
                whatsapp=instance.whatsapp,
                email=instance.email,
                assigned_employee=instance.assigned_to,
                status='Active',
                notes=f"Auto-converted from Lead. Remarks: {instance.remarks or ''}"
            )

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'company', 'college', 'contact_person']
    ordering_fields = ['created_at', 'relationship_score']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all().order_by('-created_at')
    serializer_class = ProposalSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'client__name']
    ordering_fields = ['created_at', 'training_cost']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        client_id = self.request.query_params.get('client')
        if status:
            queryset = queryset.filter(status=status)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset

class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all().order_by('-created_at')
    serializer_class = ActivityLogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        lead_id = self.request.query_params.get('lead')
        client_id = self.request.query_params.get('client')
        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all().order_by('-created_at')
    serializer_class = CollegeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'district', 'state']
    ordering_fields = ['created_at', 'name']

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all().order_by('-created_at')
    serializer_class = TrainingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'college__name', 'trainer__username']
    ordering_fields = ['created_at', 'start_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        college_id = self.request.query_params.get('college')
        if status:
            queryset = queryset.filter(status=status)
        if college_id:
            queryset = queryset.filter(college_id=college_id)
        return queryset

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'college__name', 'email', 'phone']
    ordering_fields = ['name', 'progress_percentage']

    def get_queryset(self):
        queryset = super().get_queryset()
        college_id = self.request.query_params.get('college')
        placement = self.request.query_params.get('placement_status')
        if college_id:
            queryset = queryset.filter(college_id=college_id)
        if placement:
            queryset = queryset.filter(placement_status=placement)
        return queryset

class PersonalStudentViewSet(viewsets.ModelViewSet):
    queryset = PersonalStudent.objects.all().order_by('-created_at')
    serializer_class = PersonalStudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student_name', 'certification_name']
    ordering_fields = ['created_at', 'fees']

    def get_queryset(self):
        queryset = super().get_queryset()
        payment = self.request.query_params.get('payment_status')
        cert = self.request.query_params.get('certificate_status')
        if payment:
            queryset = queryset.filter(payment_status=payment)
        if cert:
            queryset = queryset.filter(certificate_status=cert)
        return queryset
