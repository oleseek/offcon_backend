from rest_framework import viewsets, generics, serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Project, Service, News, Review, Request, SiteSettings, AboutSettings, FooterSettings, SocialLink, ContactSettings, PrivacyPolicy, ServicesBanner, ReviewQuote, TeamMember, FAQ
from .serializers import (
    ProjectSerializer, ServiceSerializer, NewsSerializer, ReviewSerializer, RequestSerializer,
    SiteSettingsSerializer, AboutSettingsSerializer, FooterSettingsSerializer, SocialLinkSerializer,
    ContactSettingsSerializer, PrivacyPolicySerializer, ServicesBannerSerializer, ReviewQuoteSerializer, TeamMemberSerializer, FAQSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.generics import DestroyAPIView, UpdateAPIView

# ========== СЕРИАЛИЗАТОР ПОЛЬЗОВАТЕЛЯ (ОПРЕДЕЛЯЕМ РАНЬШЕ, ЧЕМ ИСПОЛЬЗОВАТЬ) ==========
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# ========== ПУБЛИЧНЫЕ ЭНДПОИНТЫ (ДОСТУПНЫ БЕЗ ТОКЕНА) ==========
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filterset_fields = ['project_type', 'style']

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer

class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Review.objects.filter(is_published=True)
    serializer_class = ReviewSerializer

class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

class AboutSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = AboutSettings.objects.all()
    serializer_class = AboutSettingsSerializer

class FooterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FooterSettings.objects.all()
    serializer_class = FooterSettingsSerializer

class SocialLinkViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = SocialLink.objects.all().order_by('order')
    serializer_class = SocialLinkSerializer

class ContactSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = ContactSettings.objects.all()
    serializer_class = ContactSettingsSerializer

class PrivacyPolicyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer

class ServicesBannerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = ServicesBanner.objects.all()
    serializer_class = ServicesBannerSerializer

class ReviewQuoteView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = ReviewQuote.objects.all()
    serializer_class = ReviewQuoteSerializer

    def get_object(self):
        obj, created = ReviewQuote.objects.get_or_create(id=1)
        return obj

class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class RequestCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RequestSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)

# ========== РЕГИСТРАЦИЯ (ДОСТУПНА БЕЗ ТОКЕНА) ==========
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        user = serializer.save()
        if user.email:
            Request.objects.filter(email=user.email, user__isnull=True).update(user=user)

# ========== ЭНДПОИНТЫ, ТРЕБУЮЩИЕ АВТОРИЗАЦИИ ==========
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'name': user.get_full_name() or user.username,
            'email': user.email,
        })

class UserRequestsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = Request.objects.filter(user=request.user).order_by('-created_at')
        serializer = RequestSerializer(qs, many=True)
        return Response(serializer.data)

class UserRequestDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer
    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)

class UserRequestUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer
    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)

class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    def perform_create(self, serializer):
        request_id = self.request.data.get('request_id')
        if not request_id:
            raise serializers.ValidationError({"request_id": "Обязательное поле"})
        try:
            req = Request.objects.get(id=request_id, user=self.request.user)
        except Request.DoesNotExist:
            raise serializers.ValidationError({"request_id": "Заявка не найдена"})
        if req.review_submitted:
            raise serializers.ValidationError({"request_id": "Отзыв уже оставлен"})
        serializer.save(
            client_name_ru=req.name,
            client_name_en=req.name,
            project_ru=req.question or 'Проект',
            project_en=req.question or 'Project',
            rating=self.request.data.get('rating', 5),
            text_ru=self.request.data.get('text_ru'),
            text_en=self.request.data.get('text_en', self.request.data.get('text_ru')),
            is_published=True
        )
        req.review_submitted = True
        req.save()