from django.db import models
from wagtail import fields
from wagtail.blocks import RichTextBlock
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page, StreamField
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from pages.blocks import PageContentBlock


@register_snippet
class VacancyTopContent(models.Model):
    content = StreamField([
        ('rich_text', RichTextBlock(icon='pilcrow', label='Редактор текста', features=[
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',  # heading elements
            'text-center',
            'bold', 'italic',  # bold / italic text
            'ol', 'ul',  # ordered / unordered lists
            'hr',  # horizontal rules
            'link',  # page, external and email links
            'document-link',  # links to documents
            'image',  # embedded images
            'embed',  # embedded media
            'code',  # inline code
            'superscript', 'subscript', 'strikethrough',  # text formatting
            'blockquote'  # blockquote
        ], help_text="Вводите текст и изменяйте его")),
    ], verbose_name='Контент', use_json_field=True)

    panels = [
        FieldPanel('content')
    ]

    class Meta:
        verbose_name = 'Верхний контент на странице вакансий'
        verbose_name_plural = 'Верхний контент на странице вакансий'

    def __str__(self):
        return 'Верхний контент на странице вакансий'


@register_snippet
class Employer(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    is_favorite = models.BooleanField(verbose_name='В избранном')

    search_fields = [
        index.SearchField('name'),
        index.FilterField('is_favorite')
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("is_favorite")
    ]

    class Meta:
        verbose_name = 'Работодатель'
        verbose_name_plural = 'Работодатели'
        ordering = ['name']

    def __str__(self):
        return self.name


@register_snippet
class EducationalInstitution(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    is_favorite = models.BooleanField(verbose_name='В избранном')

    search_fields = [
        index.SearchField('name'),
        index.FilterField('is_favorite')
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("is_favorite")
    ]

    class Meta:
        verbose_name = 'Учебное заведение'
        verbose_name_plural = 'Учебные заведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class EmployerVacancyPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
        verbose_name='Картинка'
    )
    body = fields.StreamField(PageContentBlock(), verbose_name='Контент', use_json_field=True)
    preview_text = fields.RichTextField(verbose_name='Превью текст', blank=True, null=True, features=[])
    employer = models.ForeignKey(
        Employer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Работодатель'
    )
    is_favorite = models.BooleanField(verbose_name='В избранном')

    template = 'base/employer-vacancy_page.html'

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('first_published_at'),
        index.FilterField('employer_id'),
        index.FilterField('is_favorite')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('body'),
        FieldPanel('preview_text'),
        FieldPanel('first_published_at'),
        FieldPanel('employer'),
        FieldPanel('is_favorite')
    ]

    class Meta:
        verbose_name = 'Вакансия работодателя'
        verbose_name_plural = 'Вакансии работодателей'
        ordering = ['-is_favorite', '-employer__is_favorite', '-first_published_at']


class EducationalInstitutionVacancyPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
        verbose_name='Картинка'
    )
    body = fields.StreamField(PageContentBlock(), verbose_name='Контент', use_json_field=True)
    preview_text = fields.RichTextField(verbose_name='Превью текст', blank=True, null=True, features=[])
    educational_institution = models.ForeignKey(
        EducationalInstitution,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Учебное заведение'
    )
    is_favorite = models.BooleanField(verbose_name='В избранном')

    template = 'base/ei-vacancy_page.html'

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('first_published_at'),
        index.FilterField('educational_institution_id'),
        index.FilterField('is_favorite')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('body'),
        FieldPanel('preview_text'),
        FieldPanel('first_published_at'),
        FieldPanel('educational_institution'),
        FieldPanel('is_favorite')
    ]

    class Meta:
        verbose_name = 'Вакансия учебного заведения'
        verbose_name_plural = 'Вакансии учебных заведений'
        ordering = ['-is_favorite', '-educational_institution__is_favorite', '-first_published_at']
