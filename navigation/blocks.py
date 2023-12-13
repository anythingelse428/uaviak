from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class LinkBlock(blocks.StructBlock):
    text = blocks.CharBlock(label='Текст ссылки')
    url = blocks.CharBlock(label='Адрес ссылки', required=None, blank=True)


class HeaderNavigationSubLinkBlock(LinkBlock):
    pass


class HeaderNavigationLinkBlock(LinkBlock):
    children = blocks.ListBlock(HeaderNavigationSubLinkBlock(), label='Дочерние ссылки')


class HeaderNavigationBlock(blocks.StructBlock):
    logo = blocks.RawHTMLBlock(label='Лого в svg формате', help_text='html-разметка')
    links = blocks.ListBlock(HeaderNavigationLinkBlock(label='Ссылка'), label='Ссылки')

    class Meta:
        template = 'blocks/header/navigation.html'


class FooterNavigationLinkBlock(LinkBlock):
    icon = blocks.RawHTMLBlock(label='Иконка в svg формате', help_text='html-разметка')


class FooterNavigationHiddenLinkBlock(LinkBlock):
    pass


class FooterNavigationBlock(blocks.StructBlock):
    links = blocks.ListBlock(FooterNavigationLinkBlock(), label='Cсылки')
    hidden_links = blocks.ListBlock(FooterNavigationHiddenLinkBlock(), label='Спрятанные ссылки')

    class Meta:
        template = 'blocks/footer/navigation.html'


class SiteMapLinkBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()
    image = ImageChooserBlock()
    url = blocks.CharBlock(default='/')
    row = blocks.StructBlock([
        ('start', blocks.IntegerBlock()),
        ('end', blocks.IntegerBlock())
    ])
    column = blocks.StructBlock([
        ('start', blocks.IntegerBlock()),
        ('end', blocks.IntegerBlock())
    ])


class SiteMapBlock(blocks.StructBlock):
    grid = blocks.StructBlock([
        ('template', blocks.StructBlock([
            ('rows', blocks.StructBlock([
                ('size', blocks.CharBlock(label='Высота ряда'))
            ], label='Ряды')),
            ('columns', blocks.StructBlock([
                ('size', blocks.CharBlock(label='Ширина колонки')),
                ('count', blocks.IntegerBlock(label='Количество'))
            ], label='Колонки'))
        ], label='Настройки шаблона')),
        ('gap', blocks.CharBlock(label='Разрыв между ячейками'))
    ])
    links = blocks.ListBlock(SiteMapLinkBlock(label='Плитка'), label='Плитки')

    class Meta:
        template = 'blocks/page/site-map.html'
