from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    TaskViewSet, CustomTokenObtainPairView, CurrentUserView,
    LeadViewSet, ClientViewSet, ProposalViewSet, ActivityLogViewSet,
    CollegeViewSet, TrainerViewSet, TrainingViewSet, StudentViewSet, PersonalStudentViewSet
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'activities', ActivityLogViewSet)
router.register(r'colleges', CollegeViewSet)
router.register(r'trainers', TrainerViewSet)
router.register(r'trainings', TrainingViewSet)
router.register(r'students', StudentViewSet)
router.register(r'personal-students', PersonalStudentViewSet)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', CurrentUserView.as_view(), name='current_user'),
    path('', include(router.urls)),
]
