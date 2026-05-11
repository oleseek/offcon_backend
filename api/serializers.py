from rest_framework import serializers
from .models import Project, Service, News, Review, Request, AboutSettings, FooterSettings, SocialLink, ContactSettings, PrivacyPolicy, ServicesBanner, ReviewQuote, TeamMember, FAQ, ProjectImage, SiteSettings


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    progress = serializers.IntegerField(read_only=True)
    class Meta:
        model = Request
        fields = '__all__'




class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'

class AboutSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSettings
        fields = '__all__'
class FooterSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterSettings
        fields = '__all__'


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'


class ContactSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSettings
        fields = '__all__'

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class ServicesBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesBanner
        fields = '__all__'

class ReviewQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewQuote
        fields = ['id', 'text_ru', 'text_en', 'author_ru', 'author_en']

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['image', 'order']

class ProjectSerializer(serializers.ModelSerializer):
    gallery_images = ProjectImageSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'