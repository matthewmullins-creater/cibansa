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
                obj.user.save()
                obj.save()
    else:
        return delete_selected_(modeladmin, request, queryset)

delete_selected.short_description = "Delete selected objects"


class CbUserProfileAdmin(admin.ModelAdmin):
    search_fields = ["first_name","last_name","phone","country","city"]
    list_display = ("user_id","first_name","last_name","phone","gender","country","city","has_photo","is_visible",
                    "get_email")
    list_filter = ("country","city","gender")
    actions = [delete_selected]

    def get_email(self,obj):
        return obj.user.email

    def delete_model(self, request, obj):
        obj.is_visible = False
        obj.user.is_active = False
        obj.user.save()
        obj.save()


class CbUserAdmin(admin.ModelAdmin):
    list_display = ("email","is_active","is_staff","date_joined")

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.profile.is_visible = False
        obj.profile.save()
        obj.save()

admin.site.register(CbUserProfile,CbUserProfileAdmin)
# admin.site.register(User,CbUserAdmin)