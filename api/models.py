from django.db import models
from django.utils import timezone
from django.conf import settings

class Project(models.Model):
    TYPE_CHOICES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('hotel', 'Отель'),
        ('resort', 'База отдыха'),
    ]
    STYLE_CHOICES = [
        ('scandi', 'Сканди'),
        ('minimalism', 'Минимализм'),
        ('loft', 'Лофт'),
        ('classic', 'Классика'),
    ]
    title_ru = models.CharField(max_length=200, verbose_name='Название (рус)')
    title_en = models.CharField(max_length=200, verbose_name='Название (англ)')
    description_ru = models.TextField(verbose_name='Описание (рус)')
    description_en = models.TextField(verbose_name='Описание (англ)')
    location = models.CharField(max_length=200, blank=True)
    area = models.IntegerField(verbose_name='Площадь (м²)')
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='apartment')
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='minimalism')
    year = models.IntegerField(verbose_name='Год', blank=True, null=True)
    image = models.ImageField(upload_to='projects/', verbose_name='Главное изображение')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    participants_ru = models.TextField(verbose_name='Участники проекта (рус)', blank=True, default='')
    participants_en = models.TextField(verbose_name='Участники проекта (англ)', blank=True, default='')
    details_ru = models.TextField(verbose_name='Детали проекта (рус)', blank=True, default='')
    details_en = models.TextField(verbose_name='Детали проекта (англ)', blank=True, default='')
    full_description_ru = models.TextField(verbose_name='Полное описание (рус)', blank=True, default='')
    full_description_en = models.TextField(verbose_name='Полное описание (англ)', blank=True, default='')
    image2 = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name='Второе изображение (730x365)')
    image3 = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name='Третье изображение (485x380)')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title_ru

class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='gallery_images',
        verbose_name='Проект'
    )
    image = models.ImageField(
        upload_to='projects/gallery/', 
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение галереи'
        verbose_name_plural = 'Изображения галереи'

class Service(models.Model):
    name_ru = models.CharField(max_length=200, verbose_name='Название (рус)')
    name_en = models.CharField(max_length=200, verbose_name='Название (англ)')
    description_ru = models.TextField(verbose_name='Описание (рус)')
    description_en = models.TextField(verbose_name='Описание (англ)')
    duration_ru = models.CharField(max_length=100, verbose_name='Срок (рус)', blank=True)
    duration_en = models.CharField(max_length=100, verbose_name='Срок (англ)', blank=True)
    examples_ru = models.TextField(verbose_name='Примеры (рус)', blank=True)
    examples_en = models.TextField(verbose_name='Примеры (англ)', blank=True)
    icon = models.FileField(upload_to='services/', blank=True, null=True, verbose_name='Иконка (SVG)')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name_ru

class News(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Заголовок (рус)')
    title_en = models.CharField(max_length=200, verbose_name='Заголовок (англ)')
    content_ru = models.TextField(verbose_name='Текст (рус)')
    content_en = models.TextField(verbose_name='Текст (англ)')
    full_content_ru = models.TextField(verbose_name='Полный текст новости (рус)', blank=True)
    full_content_en = models.TextField(verbose_name='Полный текст новости (англ)', blank=True)
    date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title_ru

class Review(models.Model):
    client_name_ru = models.CharField(max_length=200, verbose_name='Имя клиента (рус)', default='', blank=True)
    client_name_en = models.CharField(max_length=200, verbose_name='Имя клиента (англ)', default='', blank=True)
    text_ru = models.TextField(verbose_name='Текст отзыва (рус)')
    text_en = models.TextField(verbose_name='Текст отзыва (англ)')
    project_ru = models.CharField(max_length=200, blank=True, verbose_name='Название проекта (рус)', default='')
    project_en = models.CharField(max_length=200, blank=True, verbose_name='Название проекта (англ)', default='')
    rating = models.IntegerField(default=5, verbose_name='Рейтинг (1-5)')
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.client_name_ru

class Request(models.Model):
    CONTACT_METHOD = [
        ('telegram', 'Написать в Telegram'),
        ('call', 'Позвонить по телефону'),
    ]
    STATUS_CHOICES = [
        ('sent', 'Отправлен запрос'),
        ('discussed', 'Обсудили проект'),
        ('tz', 'Сформировано ТЗ'),
        ('in_progress', 'Проект в работе'),
        ('ready', 'Проект готов'),
    ]
    TYPE_CHOICES = [
        ('apartment', 'Квартира'),
        ('house', 'Жильё'),
        ('hotel', 'Отель'),
        ('resort', 'База отдыха'),
    ]
    STYLE_CHOICES = [
        ('scandi', 'Сканди'),
        ('minimalism', 'Минимализм'),
        ('loft', 'Лофт'),
        ('classic', 'Классика'),
    ]

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    question = models.TextField(verbose_name='Вопрос', blank=True, null=True)
    contact_method = models.CharField(max_length=20, choices=CONTACT_METHOD, default='telegram')
    consent = models.BooleanField(default=True, verbose_name='Согласие на обработку')
    created_at = models.DateTimeField(default=timezone.now)
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True, null=True, verbose_name='Тип пространства')
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, blank=True, null=True, verbose_name='Стиль')
    area = models.CharField(max_length=50, blank=True, null=True, verbose_name='Площадь, м²')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent', verbose_name='Статус')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    review_submitted = models.BooleanField(default=False, verbose_name='Отзыв уже отправлен')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    @property
    def progress(self):
        return {
            'sent': 0,
            'discussed': 25,
            'tz': 50,
            'in_progress': 75,
            'ready': 100,
        }.get(self.status, 0)

    def __str__(self):
        return f"{self.name} ({self.created_at.strftime('%d.%m.%Y')})"

class SiteSettings(models.Model):
    banner_image = models.ImageField(upload_to='settings/', verbose_name='Изображение баннера', blank=True, null=True)
    banner_title_ru = models.CharField(max_length=200, verbose_name='Заголовок баннера (рус)', default='', blank=True)
    banner_title_en = models.CharField(max_length=200, verbose_name='Заголовок баннера (англ)', default='', blank=True)
    banner_subtitle_ru = models.CharField(max_length=200, verbose_name='Подзаголовок баннера (рус)', default='', blank=True)
    banner_subtitle_en = models.CharField(max_length=200, verbose_name='Подзаголовок баннера (англ)', default='', blank=True)
    quote_text_ru = models.TextField(verbose_name='Текст цитаты (рус)', default='', blank=True)
    quote_text_en = models.TextField(verbose_name='Текст цитаты (англ)', default='', blank=True)
    quote_author_ru = models.CharField(max_length=200, verbose_name='Автор цитаты (рус)', default='', blank=True)
    quote_author_en = models.CharField(max_length=200, verbose_name='Автор цитаты (англ)', default='', blank=True)
    promo_banner_image = models.ImageField(upload_to='settings/', verbose_name='Изображение промо-баннера', blank=True, null=True)
    promo_text_ru = models.CharField(max_length=200, verbose_name='Текст промо-баннера (рус)', default='', blank=True)
    promo_text_en = models.CharField(max_length=200, verbose_name='Текст промо-баннера (англ)', default='', blank=True)

    class Meta:
        verbose_name = 'Главная(баннеры и цитаты)'
        verbose_name_plural = 'Главная(баннеры и цитаты)'

    def __str__(self):
        return "Настройки сайта"

class AboutSettings(models.Model):
    image = models.ImageField(upload_to='about/', verbose_name='Фото руководителя', blank=True, null=True)
    name_ru = models.CharField(max_length=200, verbose_name='Имя (рус)', default='', blank=True)
    name_en = models.CharField(max_length=200, verbose_name='Имя (англ)', default='', blank=True)
    position_ru = models.CharField(max_length=200, verbose_name='Должность (рус)', default='', blank=True)
    position_en = models.CharField(max_length=200, verbose_name='Должность (англ)', default='', blank=True)
    quote_ru = models.CharField(max_length=200, verbose_name='Цитата (рус)', default='', blank=True)
    quote_en = models.CharField(max_length=200, verbose_name='Цитата (англ)', default='', blank=True)
    text_ru = models.TextField(verbose_name='Текст (рус)', default='', blank=True)
    text_en = models.TextField(verbose_name='Текст (англ)', default='', blank=True)
    page_text_ru = models.TextField(verbose_name='Текст на странице "О бюро" (рус)', blank=True, default='')
    page_text_en = models.TextField(verbose_name='Текст на странице "О бюро" (англ)', blank=True, default='')

    class Meta:
        verbose_name = 'О бюро'
        verbose_name_plural = 'О бюро'

    def __str__(self):
        return "Настройки раздела О бюро"

class FooterSettings(models.Model):
    address_ru = models.CharField(max_length=255, verbose_name='Адрес (рус)')
    address_en = models.CharField(max_length=255, verbose_name='Адрес (англ)')
    address_map_url = models.URLField(blank=True, verbose_name='Ссылка на карту')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=50, verbose_name='Телефон (для отображения)')
    phone_raw = models.CharField(max_length=20, blank=True, verbose_name='Телефон для ссылки (без пробелов)')
    inn_ru = models.CharField(max_length=255, verbose_name='ИНН (рус)')
    inn_en = models.CharField(max_length=255, verbose_name='ИНН (англ)')

    class Meta:
        verbose_name = 'Настройка футера'
        verbose_name_plural = 'Настройки футера'

    def __str__(self):
        return "Настройки футера"

class SocialLink(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название (VK, YouTube и т.д.)')
    url = models.URLField(verbose_name='Ссылка')
    icon = models.FileField(
        upload_to='social_icons/',
        verbose_name='Иконка (SVG)',
        help_text='Загрузите SVG‑файл'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Социальная сети ссылка'
        verbose_name_plural = 'Социальные сети ссылки'

    def __str__(self):
        return self.name

class ContactSettings(models.Model):
    address_ru = models.CharField(max_length=255, verbose_name='Адрес (рус)')
    address_en = models.CharField(max_length=255, verbose_name='Адрес (англ)')
    address_map_url = models.URLField(blank=True, verbose_name='Ссылка на карту')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=50, verbose_name='Телефон (для отображения)')
    phone_raw = models.CharField(max_length=20, blank=True, verbose_name='Телефон для ссылки (без пробелов)')
    legal_name_ru = models.CharField(max_length=255, verbose_name='Юридическое название (рус)')
    legal_name_en = models.CharField(max_length=255, verbose_name='Юридическое название (англ)')
    inn_ru = models.CharField(max_length=100, verbose_name='ИНН (рус)')
    inn_en = models.CharField(max_length=100, verbose_name='ИНН (англ)')

    class Meta:
        verbose_name = 'Контактная настройка'
        verbose_name_plural = 'Контактные настройки'

    def __str__(self):
        return "Контактные настройки"

class PrivacyPolicy(models.Model):
    text_ru = models.TextField(verbose_name='Текст политики (рус)')
    text_en = models.TextField(verbose_name='Текст политики (англ)')

    class Meta:
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = 'Политика конфиденциальности'

    def __str__(self):
        return "Политика конфиденциальности"

class ServicesBanner(models.Model):
    image = models.ImageField(upload_to='services_banner/', verbose_name='Фото баннера')
    text_ru = models.CharField(max_length=255, verbose_name='Текст баннера (рус)')
    text_en = models.CharField(max_length=255, verbose_name='Текст баннера (англ)')

    class Meta:
        verbose_name = 'Баннер (Услуги)'
        verbose_name_plural = 'Баннер (Услуги)'

    def __str__(self):
        return "Баннер страницы Услуги"

class ReviewQuote(models.Model):
    text_ru = models.TextField('Текст цитаты (ru)', blank=True)
    text_en = models.TextField('Текст цитаты (en)', blank=True)
    author_ru = models.CharField('Автор цитаты (ru)', max_length=255, blank=True)
    author_en = models.CharField('Автор цитаты (en)', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Цитата для страницы "Отзывы"'
        verbose_name_plural = 'Цитата для страницы "Отзывы"'

    def __str__(self):
        return "Цитата для страницы отзывов"

class TeamMember(models.Model):
    image = models.ImageField(upload_to='team/', verbose_name='Фото')
    name_ru = models.CharField(max_length=200, verbose_name='Имя (рус)')
    name_en = models.CharField(max_length=200, verbose_name='Имя (англ)')
    position_ru = models.CharField(max_length=200, verbose_name='Должность (рус)')
    position_en = models.CharField(max_length=200, verbose_name='Должность (англ)')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники (другие)'

    def __str__(self):
        return self.name_ru

class FAQ(models.Model):
    question_ru = models.TextField(verbose_name='Вопрос (рус)')
    question_en = models.TextField(verbose_name='Вопрос (англ)')
    answer_ru = models.TextField(verbose_name='Ответ (рус)')
    answer_en = models.TextField(verbose_name='Ответ (англ)')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.question_ru[:50]