# image_formats.py
from wagtail.images.formats import Format, register_image_format, unregister_image_format

unregister_image_format('left')
unregister_image_format('right')
unregister_image_format('fullwidth')

register_image_format(Format('originalwidth', 'На ширину изображения', 'richtext-image original-width', 'original'))
register_image_format(Format('fullwidth', 'На всю ширину', 'richtext-image full-width', 'original'))