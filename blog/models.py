from django.db import models
from wagtail import fields
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from pages.blocks import PageContentBlock


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')

    panels = [
        FieldPanel("name")
    ]

    class Meta:
        verbose_name = 'Категория Статьи'
        verbose_name_plural = 'Категории Статей'
        ordering = ['name']

    def __str__(self):
        return self.name


class ArticlePage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
        verbose_name='Картинка'
    )
    body = fields.StreamField(PageContentBlock(), verbose_name='Контент', use_json_field=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория'
    )

    template = 'base/article_page.html'

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('first_published_at'),
        index.FilterField('category_id')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('body'),
        FieldPanel('first_published_at'),
        FieldPanel('category')
    ]

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-first_published_at']
