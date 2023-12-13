from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)
from .models import Category, ArticlePage


class CategoryAdmin(ModelAdmin):
    model = Category
    base_url_path = 'categories' # customise the URL from default to admin/bookadmin
    menu_label = 'Категории'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder-open-1'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name',)
    search_fields = ('name',)


class ArticleAdmin(ModelAdmin):
    model = ArticlePage
    base_url_path = 'articles' # customise the URL from default to admin/bookadmin
    menu_label = 'Статьи'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('title', 'category', 'first_published_at', 'last_published_at', 'latest_revision_created_at')
    list_filter = ('category',)
    search_fields = ('title',)


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(CategoryAdmin)
modeladmin_register(ArticleAdmin)
