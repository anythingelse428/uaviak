from wagtail import blocks
from wagtail.blocks import RichTextBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from blog.blocks import NewsSliderBlock, ArticlesListBlock
from svo.blocks import DeceasedListBlock
from vacancies.blocks import EmployerVacanciesListBlock, EducationalInstitutionVacanciesListBlock

# Spacer Block
from navigation.blocks import SiteMapBlock


class SpacerBlock(blocks.StructBlock):
    height = blocks.CharBlock(label='Размер вертикального разрыва')

    class Meta:
        template = 'blocks/spacer.html'


# Contact Block
class ContactBlock(blocks.StructBlock):
    icon = blocks.RawHTMLBlock(label='Иконка в svg формате', help_text='html-разметка')
    text = blocks.TextBlock(label='Текст')


# Image Contact Block
class ImageContactBlock(blocks.StructBlock):
    icon = blocks.RawHTMLBlock(label='Иконка в svg формате', help_text='html-разметка')
    image = ImageChooserBlock(label='Изображение')


# Search Block
class SearchBlock(blocks.StructBlock):
    action_url = blocks.CharBlock(label='Место действия', help_text='Ссылка на страницу, на которой применится поиск')
    hint = blocks.CharBlock(label='Подсказка')


# Social Link Block
class SocialLinkBlock(blocks.StructBlock):
    icon = blocks.RawHTMLBlock(label='Иконка в svg формате', help_text='html-разметка')
    code = blocks.CharBlock(label='Код социальной сети')
    url = blocks.CharBlock(label='Адрес ссылки')


# Header Meta Block
class HeaderMetaBlock(blocks.StructBlock):
    columns = blocks.StreamBlock([
        ('contact', ContactBlock(label='Блок с иконкой и текстом')),
        ('contact_image', ImageContactBlock(label='Блок с иконкой и изображением')),
        ('search', SearchBlock(label='Поиск')),
        ('social_link', SocialLinkBlock(label='Иконка с ссылкой'))
    ], label='Колонки')

    class Meta:
        template = 'blocks/header/meta.html'


# Footer Meta Block
class FooterMetaColumnBlock(blocks.StructBlock):
    title = blocks.RichTextBlock(label='Заголовок')
    content = blocks.StreamBlock([
        ('text', blocks.RichTextBlock(label='Текстовое поле')),
        ('contacts', blocks.ListBlock(ContactBlock(label='Элемент списка'), label='Список контактов')),
        ('different_contacts', blocks.StreamBlock([
            ('contact', ContactBlock(label='Блок с иконкой и текстом')),
            ('contact_image', ImageContactBlock(label='Блок с иконкой и изображением'))
        ], label='Поток контактов'))
    ], max_num=1, label='Контент')


class FooterMetaBlock(blocks.StructBlock):
    columns = blocks.ListBlock(FooterMetaColumnBlock(), label='Колонки')

    class Meta:
        template = 'blocks/footer/meta.html'


# Banner Block
class BannerBlock(blocks.StructBlock):
    image = ImageChooserBlock(label='Изображение')
    label = blocks.CharBlock(label='Подпись', required=False)
    url = blocks.CharBlock(label='Адрес ссылки')

    class Meta:
        template = 'blocks/page/banner.html'


# Banners Slider Block
class BannersSliderBlock(blocks.StructBlock):
    banners = blocks.ListBlock(BannerBlock(label='Баннер'), label='Список баннеров')

    class Meta:
        template = 'blocks/page/banners-slider.html'


# Images Slider Block
class ImagesSliderBlock(blocks.StructBlock):
    images = blocks.ListBlock(ImageChooserBlock(label='Изображение'), label='Список изображений')

    class Meta:
        template = 'blocks/page/images-slider.html'


# Government Services Banner Block
class GovernmentServicesBannerBlock(blocks.StructBlock):
    title = blocks.CharBlock(label='Заголовок')
    sub_title = blocks.CharBlock(label='Подзаголовок')
    button = blocks.StructBlock([
        ('text', blocks.CharBlock(label='Текст'))
    ], label='Кнопка')
    background_image = ImageChooserBlock(label='Задний план баннера', required=False, blank=True)
    
    class Meta:
        template = 'blocks/page/government-services-banner.html'


# Map Block
class MapBlock(blocks.StructBlock):
    logo = blocks.RawHTMLBlock(label='Лого в формате svg', help_text='html-разметка')
    url = blocks.CharBlock(label='Ссылка на карту')
    text = blocks.RichTextBlock(label='Текст для карты')
    social = blocks.StructBlock([
        ('icon', blocks.RawHTMLBlock(label='Иконка в svg формате', help_text='html-разметка')),
        ('url', blocks.CharBlock(label='Ссылка'))
    ], label='Информация социальной сети')

    class Meta:
        template = 'blocks/page/map.html'


# Partners Block
class PartnerBlock(blocks.StructBlock):
    logo = ImageChooserBlock(label='Лого')
    name = blocks.RichTextBlock(label='Название')
    url = blocks.CharBlock(label='Ссылка')


class PartnersBlock(blocks.StructBlock):
    partners = blocks.ListBlock(PartnerBlock(label='Партнёр'), label='Список партнёров')

    class Meta:
        template = 'blocks/page/partners.html'


# Section Title Block
class SectionTitleBlock(blocks.StructBlock):
    text = blocks.CharBlock(label='Текст')

    class Meta:
        template = 'blocks/page/section-title.html'


# Patriotic Section Title Block
class PatrioticSectionTitleBlock(blocks.StructBlock):
    text = blocks.CharBlock(label='Текст')

    class Meta:
        template = 'blocks/page/patriotic-section-title.html'


# Patriotic Line Block
class PatrioticLineBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/page/patriotic-line.html'


# Statistics Banner Block
class StatisticElementBlock(blocks.StructBlock):
    value = blocks.CharBlock(label='Значение')
    description = blocks.CharBlock(label='Описание')


class StatisticsBannerBlock(blocks.StructBlock):
    statistics = blocks.ListBlock(StatisticElementBlock(label='Элемент Статистики'))
    image = ImageChooserBlock(label='Заднее изображение баннера')

    class Meta:
        template = 'blocks/page/statistics-banner.html'


# Page Content Block
class PageContentBlock(blocks.StreamBlock):
    spacer = SpacerBlock(icon='arrows-up-down', label='Разрыв контента', help_text='Отступ между элементами')
    section_title = SectionTitleBlock(icon='title', label='Название секции', help_text='Название секции')
    patriotic_section_title = PatrioticSectionTitleBlock(
        icon='title',
        label='Патриотичное название секции',
        help_text='Патриотичное название секции'
    )
    patriotic_line = PatrioticLineBlock(
        icon='horizontal-rule',
        label='Патриотичная линия',
        help_text='Патриотичная линия'
    )
    rich_text = RichTextBlock(icon='pilcrow', label='Редактор текста',
                              features=[
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
                              ],
                              help_text="Вводите текст и изменяйте его")
    embed = EmbedBlock(label="Встраиваемая ссылка", help_text="Ссылка на видео, твиты или что-нибудь подобное")
    banner = BannerBlock(icon='image', label='Баннер', help_text='Блок с картинкой')
    banners_slider = BannersSliderBlock(icon='folder-open-1', label='Карусель баннеров',
                                        help_text='Список баннеров')
    images_slider = ImagesSliderBlock(icon='folder-open-2', label='Карусель изображений', help_text='Список блочных картинок(слайдер)')
    government_services_banner = GovernmentServicesBannerBlock(icon='form', label='Государственный баннер',
                                                               help_text='Баннер госуслуг')
    map = MapBlock(icon='site', label='Карта', help_text='Гугл карта с данными')
    partners = PartnersBlock(icon='group', label='Партнёры', help_text='Список партнёров')
    statistics_banner = StatisticsBannerBlock(icon='image', label='Статистический Баннер',
                                              help_text='Баннер со статистикой')
    news_slider = NewsSliderBlock(icon='folder-open-1', label='Карусель новостей')
    articles_list = ArticlesListBlock(icon='list-ol', label='Список статей')
    employer_vacancies_list = EmployerVacanciesListBlock(icon='list-ol', label='Список вакансий работодателей')
    educational_institution_vacancies_list = EducationalInstitutionVacanciesListBlock(
        icon='list-ol', label='Список вакансий учебных учреждений'
    )
    deceased_list = DeceasedListBlock(icon='group', label='Список усопших')
    table = TableBlock(
        label='Таблица',
        table_options={
            'minSpareRows': 0,
            'startRows': 1,
            'startCols': 1,
            'preventOverflow': 'vertical',
            'renderer': 'html',
            'contextMenu': [
                'row_above',
                'row_below',
                '---------',
                'col_left',
                'col_right',
                '---------',
                'remove_row',
                'remove_col',
                '---------',
                'undo',
                'redo',
                '---------',
                'copy',
                'cut'
                '---------',
                'alignment'
            ]
        }
    )
    typed_table = TypedTableBlock([
            ('text', blocks.CharBlock()),
            ('numeric', blocks.FloatBlock()),
            ('rich_text', blocks.RichTextBlock()),
            ('image', ImageChooserBlock())
        ],
        label='Таблица V2',
        table_options={
            'preventOverflow': 'horizontal',
            'contextMenu': [
                'row_above',
                'row_below',
                '---------',
                'col_left',
                'col_right',
                '---------',
                'remove_row',
                'remove_col',
                '---------',
                'undo',
                'redo',
                '---------',
                'copy',
                'cut'
                '---------',
                'alignment'
            ]
        }
    )
    site_map = SiteMapBlock(icon='site', label='Карта сайта', help_text='Дополнительные ссылки')
    partners = PartnersBlock(icon='list-ul', label='Список партнёров')
    raw_html = blocks.RawHTMLBlock(label='Html', help_text='Html-код')
