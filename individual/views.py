from rest_framework import viewsets
from rest_framework.views import APIView

from .models import IndividualProfile, Address, ExperienceDetail, JobCategory, JobLevel, EducationDetail, TrainingDetail, \
    ProjectDetail, SkillSet, SeekerSkillSet, SocialNetwork
from jobs.models import JobPost
from .serializers import IndividualProfileSerializer, AddressSerializer, ExperienceDetailSerializer, JobCategorySerializer, \
    JobLevelSerializer, EducationDetailSerializer, ProjectDetailSerializer, TrainingDetailSerializer, \
    SkillSetSerializer, SeekerSkillSetSerializer, SocialNetworkSerializer
from jobs.serializers import JobPostSerializer
from rest_framework import filters, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsIndividual, IsIndividualProvider, IndividualProfileEditPermission


class IndividualProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsIndividual, IndividualProfileEditPermission]
    queryset = IndividualProfile.objects.all()
    serializer_class = IndividualProfileSerializer

    def get_queryset(self):
        queryset = self.get_serializer_class().setup_eager_loading(self.queryset)
        return queryset


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class JobCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer


class JobLevelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = JobLevel.objects.all()
    serializer_class = JobLevelSerializer


class ExperienceDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = ExperienceDetail.objects.all()
    serializer_class = ExperienceDetailSerializer

    def get_queryset(self):
        queryset = self.get_serializer_class().setup_eager_loading(self.queryset)
        return queryset


class EducationDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = EducationDetail.objects.all()
    serializer_class = EducationDetailSerializer


class ProjectDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = ProjectDetail.objects.all()
    serializer_class = ProjectDetailSerializer


class TrainingDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = TrainingDetail.objects.all()
    serializer_class = TrainingDetailSerializer


class SkillSetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = SkillSet.objects.all()
    serializer_class = SkillSetSerializer


class SeekerSkillSetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = SeekerSkillSet.objects.all()
    serializer_class = SeekerSkillSetSerializer


class SocialNetworkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsIndividual, IndividualProfileEditPermission]
    queryset = SocialNetwork.objects.all()
    serializer_class = SocialNetworkSerializer


class Resume(APIView):

    def get(self, request, format=None):
        serializer_list = []
        user = self.request.user
        profile = IndividualProfile.objects.filter(user_id=user.id).all()
        experience = ExperienceDetail.objects.filter(
            user_id=user.id).all()
        education = EducationDetail.objects.filter(
            user_id=user.id).all()
        project = ProjectDetail.objects.filter(
            user_id=user.id).all()
        training = TrainingDetail.objects.filter(
            user_id=user.id).all()
        profile_serializer = IndividualProfileSerializer(profile, many=True)
        experience_serializer = ExperienceDetailSerializer(
            experience, many=True)
        education_serializer = EducationDetailSerializer(education, many=True)
        project_serializer = ProjectDetailSerializer(project, many=True)
        training_serializer = TrainingDetailSerializer(training, many=True)
        serializer_list.extend([profile_serializer.data, experience_serializer.data, education_serializer.data,
                                project_serializer.data, training_serializer.data])

        return Response(serializer_list)


# Search Filter
class SearchListView(generics.ListAPIView):
    queryset = TrainingDetail.objects.all()
    serializer_class = TrainingDetailSerializer
    filter_backends = [filters.SearchFilter]
    print(filters.SearchFilter)
    search_fields = ['^course_name']


# Recommend System
class RecommendJobs(APIView):

    def get(self, request, format=None):
        user = self.request.user
        user_course = TrainingDetail.objects.filter(
            seeker_profile__user__id=user.id).all()
        print(user_course)
        serializer_list = []
        for course in user_course:
            users_course = course.course_name
            recommend_jobs = JobPost.objects.filter(
                job_type__job_type=users_course).all()
            serializer = JobPostSerializer(recommend_jobs, many=True)
            serializer_list.append(serializer.data)
        return Response(serializer_list)
