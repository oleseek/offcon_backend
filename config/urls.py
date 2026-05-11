from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from api.views import ProjectViewSet, ServiceViewSet, NewsViewSet, ReviewViewSet, RequestCreateView
from api.views import SiteSettingsViewSet
from api.views import AboutSettingsViewSet
from api.views import FooterViewSet, SocialLinkViewSet
from api.views import ContactSettingsViewSet
from api.views import PrivacyPolicyViewSet
from api.views import ServicesBannerViewSet
from api.views import ReviewQuoteView
from api.views import TeamMemberViewSet, FAQViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import UserProfileView, UserRequestsView, RegisterView  
from api.views import UserRequestDeleteView
from api.views import UserRequestUpdateView
from api.views import ReviewCreateView


router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('services', ServiceViewSet)
router.register('news', NewsViewSet)
router.register('reviews', ReviewViewSet)
router.register('settings', SiteSettingsViewSet)
router.register('about-settings', AboutSettingsViewSet)  
router.register(r'footer-settings', FooterViewSet, basename='footer-settings')
router.register(r'social-links', SocialLinkViewSet, basename='social-links')
router.register(r'contact-settings', ContactSettingsViewSet, basename='contact-settings')
router.register(r'privacy-policy', PrivacyPolicyViewSet, basename='privacy-policy')
router.register(r'services-banner', ServicesBannerViewSet, basename='services-banner')
router.register('team-members', TeamMemberViewSet)
router.register('faq', FAQViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/review-quote/', ReviewQuoteView.as_view(), name='review-quote'),
    path('api/requests/', RequestCreateView.as_view(), name='request-create'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/me/', UserProfileView.as_view(), name='user-me'),
    path('api/user/requests/', UserRequestsView.as_view(), name='user-requests'),
    path('api/register/', RegisterView.as_view()),
    path('api/user/requests/<int:pk>/', UserRequestDeleteView.as_view(), name='user-request-delete'),
    path('api/user/requests/<int:pk>/update/', UserRequestUpdateView.as_view(), name='user-request-update'),
    path('api/feedback/', ReviewCreateView.as_view(), name='review-create'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)