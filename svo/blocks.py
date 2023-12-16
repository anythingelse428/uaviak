from wagtail import blocks


class DeceasedListBlock(blocks.StructBlock):
    def get_context(self, value, parent_context=None):
        from svo.models import DeceasedPage

        context = super().get_context(value, parent_context=parent_context)
        context['self']['persons'] = DeceasedPage.objects.live().order_by('-first_published_at')
        return context

    class Meta:
        template = 'blocks/blog/deceased-list.html'
