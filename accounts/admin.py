from django.contrib import admin
from accounts.models import CbUserProfile,User

# Register your models here.

class CbUserAdmin(admin.ModelAdmin):
    search_fields = ["first_name","last_name","phone","country","city"]
    list_display = ("user_id","first_name","last_name","phone","gender","country","city","has_photo")


admin.site.register(CbUserProfile,CbUserAdmin)