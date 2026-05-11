from django.contrib import admin
from django import forms  # <-- добавили импорт forms
from .models import Project, Service, News, Review, Request, SiteSettings, AboutSettings, FooterSettings, SocialLink, ContactSettings, PrivacyPolicy, ServicesBanner, ReviewQuote, TeamMember, FAQ, ProjectImage 

# Убираем лишнюю регистрацию SocialLink (она будет через декоратор)
# admin.site.register(SocialLink)  <-- удалите или закомментируйте эту строку

admin.site.register(FooterSettings)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'order')
    list_editable = ('order',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'date', 'is_published')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name_ru', 'project_ru', 'rating', 'is_published')
    list_filter = ('rating', 'is_published')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'status', 'progress')
    list_filter = ('status', 'contact_method')  # убрали 'progress'

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Баннер', {
            'fields': ('banner_image', 'banner_title_ru', 'banner_title_en', 'banner_subtitle_ru', 'banner_subtitle_en')
        }),
        ('Цитата', {
            'fields': ('quote_text_ru', 'quote_text_en', 'quote_author_ru', 'quote_author_en')
        }),
        ('Промо-баннер', {
            'fields': ('promo_banner_image', 'promo_text_ru', 'promo_text_en')
        }),
    )
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(AboutSettings)
class AboutSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Фото', {
            'fields': ('image',)
        }),
        ('Имя и должность', {
            'fields': ('name_ru', 'name_en', 'position_ru', 'position_en')
        }),
        ('Цитата', {
            'fields': ('quote_ru', 'quote_en')
        }),
        ('Текст', {
            'fields': ('text_ru', 'text_en')
        }),
        ('Текст на странице "О бюро"', {
            'fields': ('page_text_ru', 'page_text_en')
        }),
    )
    def has_add_permission(self, request):
        if AboutSettings.objects.exists():
            return False
        return super().has_add_permission(request)

# Теперь используем forms.ModelForm и forms.FileInput
class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = '__all__'
        widgets = {
            'icon': forms.FileInput(attrs={'accept': '.svg'})
        }
    
    def clean_icon(self):
        icon = self.cleaned_data['icon']
        if not icon.name.endswith('.svg'):
            raise forms.ValidationError('Можно загружать только SVG файлы')
        return icon

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    form = SocialLinkForm
    list_display = ('name', 'url', 'order')
    list_editable = ('order',)

@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Адрес', {
            'fields': ('address_ru', 'address_en', 'address_map_url')
        }),
        ('Контакты', {
            'fields': ('email', 'phone', 'phone_raw')
        }),
        ('Юридическая информация', {
            'fields': ('legal_name_ru', 'legal_name_en', 'inn_ru', 'inn_en')
        }),
    )
    def has_add_permission(self, request):
        # Разрешить добавлять только если нет ни одной записи
        if ContactSettings.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Русский', {'fields': ('text_ru',)}),
        ('English', {'fields': ('text_en',)}),
    )
    def has_add_permission(self, request):
        # Разрешить добавлять только если нет ни одной записи
        if PrivacyPolicy.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(ServicesBanner)
class ServicesBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_ru', 'text_en')
    fieldsets = (
        ('Изображение', {'fields': ('image',)}),
        ('Текст (русский)', {'fields': ('text_ru',)}),
        ('Текст (английский)', {'fields': ('text_en',)}),
    )
    def has_add_permission(self, request):
        # Разрешить добавлять только если нет ни одной записи
        if ServicesBanner.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(ReviewQuote)
class ReviewQuoteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Русская версия', {
            'fields': ('text_ru', 'author_ru')
        }),
        ('English version', {
            'fields': ('text_en', 'author_en')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'position_ru', 'order')
    list_editable = ('order',)
    fieldsets = (
        ('Фото', {'fields': ('image',)}),
        ('Русский', {'fields': ('name_ru', 'position_ru')}),
        ('English', {'fields': ('name_en', 'position_en')}),
        ('Порядок', {'fields': ('order',)}),
    )

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_ru', 'order')
    list_editable = ('order',)
    fieldsets = (
        ('Русский', {'fields': ('question_ru', 'answer_ru')}),
        ('English', {'fields': ('question_en', 'answer_en')}),
        ('Порядок', {'fields': ('order',)}),
    )

class ProjectImageInline(admin.TabularInline):  # TabularInline сделает интерфейс в виде таблицы
    model = ProjectImage
    extra = 1  # Количество пустых строк для новых изображений
    fields = ('image', 'order')  # Поля, которые будут видны

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'project_type', 'style', 'area', 'year')
    list_filter = ('project_type', 'style')
    inlines = [ProjectImageInline]  # Связываем Inline с моделью Project