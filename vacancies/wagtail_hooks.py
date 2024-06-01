from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)
from .models import Employer, EmployerVacancyPage, EducationalInstitution, EducationalInstitutionVacancyPage


class EmployerAdmin(ModelAdmin):
    model = Employer
    base_url_path = 'employers' # customise the URL from default to admin/bookadmin
    menu_label = 'Работодатели'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder-open-1'  # change as required
    menu_order = 301  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'is_favorite')
    search_fields = ('name',)


class EmployerVacancyPageAdmin(ModelAdmin):
    model = EmployerVacancyPage
    base_url_path = 'employer-vacancies'  # customise the URL from default to admin/bookadmin
    menu_label = 'Вакансии работодателей'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 302  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('title', 'employer', 'first_published_at', 'last_published_at', 'latest_revision_created_at')
    list_filter = ('employer',)
    search_fields = ('title',)


class EducationalInstitutionAdmin(ModelAdmin):
    model = EducationalInstitution
    base_url_path = 'educational-institutions' # customise the URL from default to admin/bookadmin
    menu_label = 'Учебные заведения'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder-open-1'  # change as required
    menu_order = 303  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'is_favorite')
    search_fields = ('name',)


class EducationalInstitutionVacancyPageAdmin(ModelAdmin):
    model = EducationalInstitutionVacancyPage
    base_url_path = 'ei-vacancies'  # customise the URL from default to admin/bookadmin
    menu_label = 'Вакансии учебных заведений'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 304  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = (
        'title', 'educational_institution', 'first_published_at', 'last_published_at', 'latest_revision_created_at'
    )
    list_filter = ('educational_institution',)
    search_fields = ('title',)


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(EmployerAdmin)
modeladmin_register(EmployerVacancyPageAdmin)
modeladmin_register(EducationalInstitutionAdmin)
modeladmin_register(EducationalInstitutionVacancyPageAdmin)
