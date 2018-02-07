from django.contrib import admin

from ast import  literal_eval

from .models import CbCourses
# from .models import CbCoursesTags
from main.models import  CbTag
from courses.forms import CbCoursesAdminForm

class CbArticleAdmin(admin.ModelAdmin):
    list_display = ("title","category","created_at","user","is_visible")
    form = CbCoursesAdminForm
    search_fields = ("title","category","user__profile__first_name","user__profile__last_name","")
    list_filter = ("user","category","created_at","is_visible")
    # actions = None

    def save_model(self, request, obj, form, change):
        super(CbArticleAdmin, self).save_model(request, obj, form, change)
        # if form.cleaned_data.get("tag"):
        #     # obj.article_tags.all().delete()
        #     for tag in literal_eval(form.cleaned_data.get("tag")):
        #         CbCoursesTags.objects.create(
        #             article=obj,
        #             tag=CbTag.objects.get(pk=tag)
        #         )


    # def save_related(self, request, form, formsets, change):

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
            kwargs["label"] = "User *"
        if db_field.name == "category":
            kwargs["label"] = "Category *"
        return super(CbArticleAdmin,self).formfield_for_dbfield(db_field,request,**kwargs)

class CbCoursesTagAdmin(admin.ModelAdmin):
    list_display = ("courses","tag","created_at")


admin.site.register(CbCourses,CbArticleAdmin)
# admin.site.register(CbCoursesTags,CbCoursesTagAdmin)
