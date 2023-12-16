from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import fields
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.models import Page, Orderable


class DeceasedPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
        verbose_name='Изображение'
    )
    biography = fields.RichTextField(verbose_name='Биография', features=[])
    preview_biography = fields.RichTextField(verbose_name='Превью биографии', max_length=255, features=[])
    birth_date = models.DateField(verbose_name="Дата рождения")
    death_date = models.DateField(verbose_name="Дата смерти")

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('biography'),
        FieldPanel('preview_biography'),
        FieldPanel('birth_date'),
        FieldPanel('death_date'),
        MultiFieldPanel([
            InlinePanel('awards', label="Награда")],
            heading="Награды"
        ),
        MultiFieldPanel([
            InlinePanel('files', label="Файл")],
            heading="Файлы"
        ),
        FieldPanel('first_published_at'),
    ]

    template = 'base/deceased_page.html'

    class Meta:
        verbose_name = 'Усопший'
        verbose_name_plural = 'Усопшие'
        ordering = ['-first_published_at']


class DeceasedAward(Orderable):
    page = ParentalKey(DeceasedPage, on_delete=models.CASCADE, related_name='awards')
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',
        verbose_name='Изображение награды'
    )

    panels = [
        FieldPanel('image')
    ]

    class Meta:
        verbose_name = 'Награда усопшего'
        verbose_name_plural = 'Награды усопших'


class DeceasedFile(Orderable):
    page = ParentalKey(DeceasedPage, on_delete=models.CASCADE, related_name='files')
    document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',
        verbose_name='Документ файла'
    )

    panels = [
        FieldPanel('document')
    ]

    class Meta:
        verbose_name = 'Файл усопшего'
        verbose_name_plural = 'Файлы усопших'
