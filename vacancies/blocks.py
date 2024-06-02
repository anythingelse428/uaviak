from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from wagtail import blocks
from django.db.models import F


class EmployerVacanciesListBlock(blocks.StructBlock):
    page_size = blocks.IntegerBlock(
        label='Размер страницы', help_text='Количество вакансий работодателей на одной странице',
    )

    def get_context(self, value, parent_context=None):
        from vacancies.models import EmployerVacancyPage

        context = super().get_context(value, parent_context=parent_context)

        filters = {}

        queryset = EmployerVacancyPage.objects.live().order_by(
            F('is_favorite').desc(nulls_last=True),
            F('employer__is_favorite').desc(nulls_last=True),
            F('first_published_at').desc(nulls_last=True)
        )

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
        context['self']['vacancies'] = result
        if page:
            context['self']['pages'] = list(paginator.get_elided_page_range(page, on_each_side=2, on_ends=1))
            context['self']['current_page'] = page
        else:
            context['self']['pages'] = []

        context['self']['filters'] = filters

        return context

    class Meta:
        template = 'blocks/vacancies/employer-list.html'


class EducationalInstitutionVacanciesListBlock(blocks.StructBlock):
    page_size = blocks.IntegerBlock(
        label='Размер страницы', help_text='Количество вакансий учебных заведений на одной странице',
    )

    def get_context(self, value, parent_context=None):
        from vacancies.models import EducationalInstitutionVacancyPage

        context = super().get_context(value, parent_context=parent_context)

        filters = {}

        queryset = EducationalInstitutionVacancyPage.objects.live().order_by(
            F('is_favorite').desc(nulls_last=True),
            F('educational_institution__is_favorite').desc(nulls_last=True),
            F('first_published_at').desc(nulls_last=True)
        )

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
        context['self']['vacancies'] = result
        if page:
            context['self']['pages'] = list(paginator.get_elided_page_range(page, on_each_side=2, on_ends=1))
            context['self']['current_page'] = page
        else:
            context['self']['pages'] = []

        context['self']['filters'] = filters

        return context

    class Meta:
        template = 'blocks/vacancies/ei-list.html'
