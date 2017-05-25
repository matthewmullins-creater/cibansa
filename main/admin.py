from django.contrib import admin
from main.models import CbCategory,CbTag,CbTopic,CbTopicTags,CbQuestion,CbQuestionTag,CbCategoryTags
from django import forms
from main.forms import CbCategoryForm,CbTopicAdminForm,CbQuestionAdminForm
from ast import  literal_eval

# Register your models here.


class CbCategoryAdmin(admin.ModelAdmin):
    list_display = ("name","owner","created_at","owner","slug")
    search_fields = ("name",)
    form = CbCategoryForm

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "description" or db_field.name == "meta_data":
            kwargs["widget"] = forms.Textarea
        if db_field.name == "owner":
            kwargs["initial"] = request.user
        return super(CbCategoryAdmin,self).formfield_for_dbfield(db_field,request,**kwargs)

    def save_model(self, request, obj, form, change):
        super(CbCategoryAdmin, self).save_model(request, obj, form, change)
        if form.cleaned_data.get("tag"):
            obj.category_tags.all().delete()
            for tag in literal_eval(form.cleaned_data.get("tag")):
                CbCategoryTags.objects.create(
                    category=obj,
                    tag=CbTag.objects.get(pk=tag)
                )


    #
    # # def get_form(self, request, obj=None, **kwargs):
    # #     form = super(CbCategoryAdmin,self).get_form(request,obj,**kwargs)
    # #     form.owner = request.user
    # #     return form


class CbTagAdmin(admin.ModelAdmin):
    list_display = ("id","name","slug")


class CbCategoryTagsAdmin(admin.ModelAdmin):
    list_display = ("tag","category")


class CbTopicTagsAdmin(admin.ModelAdmin):
    list_display = ("tag","topic")


class CbQuestionTagsAdmin(admin.ModelAdmin):
    list_display = ("tag","question")
    search_fields = ("question",)


class CbTopicAdmin(admin.ModelAdmin):
    list_display = ("title","category","owner","slug")
    form = CbTopicAdminForm

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(CbTopicAdmin,self).get_form(request,obj,**kwargs)
    #     form.owner = request.user.id
    #     return form
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "owner":
            kwargs["initial"] = request.user
        return super(CbTopicAdmin,self).formfield_for_dbfield(db_field,request,**kwargs)

    def save_model(self, request, obj, form, change):
        super(CbTopicAdmin, self).save_model(request, obj, form, change)
        if form.cleaned_data.get("tag"):
            obj.topic_tags.all().delete()
            for tag in literal_eval(form.cleaned_data.get("tag")):
                CbTopicTags.objects.create(
                    topic=obj,
                    tag=CbTag.objects.get(pk=tag)
                )


class CbQuestionAdmin(admin.ModelAdmin):
    form=CbQuestionAdminForm
    list_display = ("title","topic","owner","created_at","updated_at","status","category")

    def save_model(self, request, obj, form, change):
        super(CbQuestionAdmin, self).save_model(request, obj, form, change)
        if form.cleaned_data.get("tag"):
            obj.question_tags.all().delete()
            for tag in literal_eval(form.cleaned_data.get("tag")):
                CbQuestionTag.objects.create(
                    question=obj,
                    tag=CbTag.objects.get(pk=tag)
                )


    # def save_related(self, request, form, formsets, change):

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "owner":
            kwargs["initial"] = request.user
        return super(CbQuestionAdmin,self).formfield_for_dbfield(db_field,request,**kwargs)


    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(CbQuestionAdmin,self).get_form(request,obj,**kwargs)
    #     print(request,request.user.id)
    #     form.owner = request.user.id
    #     return form


admin.site.register(CbCategory,CbCategoryAdmin)
admin.site.register(CbTopic,CbTopicAdmin)
admin.site.register(CbTag,CbTagAdmin)
admin.site.register(CbQuestion,CbQuestionAdmin)
admin.site.register(CbTopicTags,CbTopicTagsAdmin)
admin.site.register(CbCategoryTags,CbCategoryTagsAdmin)
admin.site.register(CbQuestionTag,CbQuestionTagsAdmin)
