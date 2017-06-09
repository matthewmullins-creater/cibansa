from django.contrib import admin
from articles.models import CbArticle, CbArticleTags
from main.models import  CbTag
from ast import  literal_eval
from articles.forms import CbArticleAdminForm
# Register your models here.


class CbArticleAdmin(admin.ModelAdmin):
    list_display = ("title","category","created_at","user")
    form = CbArticleAdminForm
    search_fields = ("title","category")

    def save_model(self, request, obj, form, change):
        super(CbArticleAdmin, self).save_model(request, obj, form, change)
        if form.cleaned_data.get("tag"):
            obj.article_tags.all().delete()
            for tag in literal_eval(form.cleaned_data.get("tag")):
                CbArticleTags.objects.create(
                    article=obj,
                    tag=CbTag.objects.get(pk=tag)
                )


    # def save_related(self, request, form, formsets, change):

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
        return super(CbArticleAdmin,self).formfield_for_dbfield(db_field,request,**kwargs)


class CbArticleTagAdmin(admin.ModelAdmin):
    list_display = ("article","tag","created_at")


admin.site.register(CbArticle,CbArticleAdmin)
admin.site.register(CbArticleTags,CbArticleTagAdmin)
