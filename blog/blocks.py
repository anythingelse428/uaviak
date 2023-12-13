from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from wagtail import blocks

from navigation.blocks import LinkBlock


class NewsSliderBlock(blocks.StructBlock):
    additional_links = blocks.ListBlock(LinkBlock(), label='Дополнительные ссылки')
    max_count = blocks.IntegerBlock(label='Максимальное количество постов в слайдере')

    def get_context(self, value, parent_context=None):
        from blog.models import ArticlePage

        context = super().get_context(value, parent_context=parent_context)
        context['self']['articles'] = ArticlePage.objects.live().order_by('-first_published_at')[:value['max_count']]
        context['self'].pop('max_count')
        return context

    class Meta:
        template = 'blocks/blog/news-carousel.html'


class ArticlesListBlock(blocks.StructBlock):
    page_size = blocks.IntegerBlock(label='Размер страницы', help_text='Количество постов на одной странице')

    def get_context(self, value, parent_context=None):
        from blog.models import ArticlePage, Category

        context = super().get_context(value, parent_context=parent_context)

        filters = {}

        queryset = ArticlePage.objects.live()

        category_id = context['request'].GET.get('category', None)
        if category_id and category_id.isdigit():
            queryset = queryset.filter(category__id=category_id)
            filters['category'] = int(category_id)

        queryset = queryset.order_by('-first_published_at')

        # Search
        search = context['request'].GET.get('search', '')
        if search != '':
            filters['search'] = search
            queryset = queryset.search(search)


        # Pagination
        page = context['request'].GET.get("page", 1)
        paginator = Paginator(queryset, value['page_size'], allow_empty_first_page=False)
        try:
            result = paginator.page(page)
            page = int(page)
        except PageNotAnInteger:
            page = 1
            result = paginator.page(page).object_list
        except EmptyPage:
            page = 1
            try:
                result = paginator.page(page).object_list
            except EmptyPage:
                page = 0
                result = []

        # Combining
        context['self']['articles'] = result
        if page:
            context['self']['pages'] = list(paginator.get_elided_page_range(page, on_each_side=2, on_ends=1))
            context['self']['current_page'] = page
        else:
            context['self']['pages'] = []

        context['self']['filters'] = filters
        context['self']['categories'] = Category.objects.all()

        return context

    class Meta:
        template = 'blocks/blog/list.html'
