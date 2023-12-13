from django import template
from pages.models import Footer, Header, BottomContent

register = template.Library()


@register.inclusion_tag('includes/header.html', takes_context=True)
def header_tag(context):
    return {
        'request': context['request'],
        'self': Header.objects.first()
    }


@register.inclusion_tag('includes/footer.html', takes_context=True)
def footer_tag(context):
    return {
        'request': context['request'],
        'self': Footer.objects.first()
    }


@register.inclusion_tag('includes/bottom-content.html', takes_context=True)
def bottom_content_tag(context):
    return {
        'request': context['request'],
        'self': BottomContent.objects.first()
    }

