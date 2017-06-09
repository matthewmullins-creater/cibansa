from django.contrib import admin
from accounts.models import CbUserProfile,User
from django.contrib.admin.actions import delete_selected as delete_selected_
from django.core.exceptions import PermissionDenied
# Register your models here.


def delete_selected(modeladmin, request, queryset):
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied
    if request.POST.get('post'):
            for obj in queryset:
                obj.is_visible = False
                obj.user.is_active = False
                obj.save()
    else:
        return delete_selected_(modeladmin, request, queryset)

delete_selected.short_description = "Delete selected objects"


class CbUserAdmin(admin.ModelAdmin):
    search_fields = ["first_name","last_name","phone","country","city"]
    list_display = ("user_id","first_name","last_name","phone","gender","country","city","has_photo","is_visible")
    actions = [delete_selected]

    def delete_model(self, request, obj):
        obj.is_visible = False
        obj.user.is_active = False
        obj.save()

admin.site.register(CbUserProfile,CbUserAdmin)