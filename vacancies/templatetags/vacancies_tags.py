from django import template
from vacancies.models import VacancyTopContent

register = template.Library()


@register.inclusion_tag('includes/vacancy-top-content.html', takes_context=True)
def vacancy_top_content_tag(context):
    return {
        'request': context['request'],
        'self': VacancyTopContent.objects.first()
    }
