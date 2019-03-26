from django.contrib import admin
from .models import Emitent, Industry, IndustrySubgroup


# ------------------Admin classes------------------

class EmitentAdminSetup(admin.ModelAdmin):
    """
    Main Emitent model's admin page
    """

    fieldsets = [
        (None, {'fields': ['publish_stage']}),
        (None, {'fields': ['name']}),
        ('Emitent ticker', {'fields': ['ticker']}),
        ('Emitent industry', {'fields': ['industry', 'industry_subgroup']}),
        ('Emitent web-site and documents urls', {'fields': ['web_site', 'documents_url']}),
        ('Emitent features', {'fields': ['main_advantages']}),
        ('Emitent short history', {'fields': ['short_history']}),
        ('Emitent additional information', {'fields': ['additional_info']}),
    ]

    list_display = ('emitent_name',
                    'emitent_admin_last_edit_time',
                    'emitent_last_editor',
                    'emitent_publish_status')

    # save model with user name
    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user
        super().save_model(request, obj, form, change)


class IndustryAdminSetup(admin.ModelAdmin):
    """
    Main Industry model's admin page
    """

    fieldsets = [
        (None, {'fields': ['publish_stage']}),
        (None, {'fields': ['industry']}),
        ('Unique url name', {'fields': ['url_name']}),
        ('Short description', {'fields': ['short_description']}),
    ]

    list_display = ('industry_name_return',
                    'publish')


class SubIndustryAdminSetup(admin.ModelAdmin):
    """
    Main Industry_subgroup model's admin page
    """

    fieldsets = [
        (None, {'fields': ['publish_stage']}),
        ('Industry groups', {'fields': ['industry']}),
        (None, {'fields': ['subgroup']}),
        ('Unique url name', {'fields': ['url_name']}),
        ('Short description', {'fields': ['short_description']}),
    ]

    list_display = ('sub_industry_name',
                    'industry_name_return',
                    'publish')


# ----------------------Registrations---------------------------

admin.site.register(Industry, IndustryAdminSetup)
admin.site.register(IndustrySubgroup, SubIndustryAdminSetup)
admin.site.register(Emitent, EmitentAdminSetup)
