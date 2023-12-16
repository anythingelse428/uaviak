from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.models import Page, StreamField, Orderable
from wagtail.snippets.models import register_snippet

from navigation.blocks import FooterNavigationBlock, HeaderNavigationBlock
from pages.blocks import PageContentBlock, FooterMetaBlock, HeaderMetaBlock


@register_snippet
class Header(models.Model):
    content = StreamField([
        ('meta', HeaderMetaBlock(icon='doc-full', label='Блок информации')),
        ('navigation', HeaderNavigationBlock(icon='list-ol', label='Блок навигации'))
    ], verbose_name='Контент шапки', use_json_field=True)

    panels = [
        FieldPanel('content')
    ]

    class Meta:
        verbose_name = 'Шапка'
        verbose_name_plural = 'Шапки'

    def __str__(self):
        return 'Шапка'


@register_snippet
class Footer(models.Model):
    content = StreamField([
        ('navigation', FooterNavigationBlock(icon='list-ol', label='Блок навигации')),
        ('meta', FooterMetaBlock(icon='doc-full', label='Блок информации'))
    ], verbose_name='Контент подвала', use_json_field=True)

    panels = [
        FieldPanel('content')
    ]

    class Meta:
        verbose_name = 'Подвал'
        verbose_name_plural = 'Подвалы'

    def __str__(self):
        return 'Подвал'


@register_snippet
class BottomContent(models.Model):
    content = StreamField(PageContentBlock(), verbose_name='Контент', use_json_field=True)

    panels = [
        FieldPanel('content')
    ]

    class Meta:
        verbose_name = 'Нижний закреплённый контент'
        verbose_name_plural = 'Нижний закреплённый контент'

    def __str__(self):
        return 'Нижний закреплённый контент'


class SimplePage(Page):
    body = StreamField(PageContentBlock(), verbose_name='Контент страницы', use_json_field=True)

    template = 'base/simple_page.html'

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    class Meta:
        verbose_name = 'Простая страница с контентом'
        verbose_name_plural = 'Простые страницы с контентом'


class ComplexPage(Page):
    template = 'base/complex_page.html'

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('tabs', label="Вкладка")],
            heading="Вкладки"
        ),
        MultiFieldPanel([
            InlinePanel('materials', label="Материал")],
            heading="Материалы"
        )
    ]

    class Meta:
        verbose_name = 'Страница с вкладками и материалами'
        verbose_name_plural = 'Страницы с вкладками и материалами'


class ComplexPageTab(Orderable):
    page = ParentalKey(ComplexPage, on_delete=models.CASCADE, related_name='tabs')
    name = models.CharField(max_length=500, blank=True, verbose_name='Название вкладки')
    body = StreamField(PageContentBlock(), verbose_name='Контент вкладки', use_json_field=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('body')
    ]

    class Meta:
        verbose_name = 'Вкладка страницы'
        verbose_name_plural = 'Вкладки страниц'


class ComplexPageMaterial(Orderable):
    page = ParentalKey(ComplexPage, on_delete=models.CASCADE, related_name='materials')
    name = models.CharField(max_length=500, verbose_name='Навзание материала')
    document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',
        verbose_name='Документ материала'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('document')
    ]

    class Meta:
        verbose_name = 'Материал страницы'
        verbose_name_plural = 'Материалы страниц'
