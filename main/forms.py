from django import forms
from main.models import CbCategory,CbQuestion,CbTag,CbQuestion,CbTopic,CbTopicTags,CbQuestionTag
from accounts.models import User
from selectable.forms import AutoCompleteSelectMultipleWidget,AutoComboboxSelectWidget,AutoCompleteSelectField
from main.lookups import TagLookup,TopicLookup
from tinymce.widgets import TinyMCE
from PIL import Image
from django.utils.translation import ugettext as _
import os
from django.db.models import Q
from django.forms import Textarea

# from  ast import literal_eval
# from django.db import transaction


class CbCategoryForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(CbCategoryForm,self).__init__(*args,**kwargs)
        users = [("", "Select user")]
        # self.fields["owner"] = self.request.user.id
        for c in User.objects.filter(is_superuser=True, is_staff=True,is_active=True):
            users.append((c.id, c.get_full_name()))
        self.fields["owner"].choices = users

    name = forms.CharField(max_length=255,label="Name *")
    image = forms.ImageField(required=False, label="Image (max size 2MB) ")
    description = forms.CharField(max_length=1024, required=False,widget=forms.Textarea)
    meta_data = forms.CharField(required=False,widget=forms.Textarea)
    # owner = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_superuser=True,is_staff=True))
    owner = forms.Select(choices=[])
    is_visible = forms.BooleanField(required=False)
    tag = forms.CharField(
        label='Type tag name',
        widget=AutoCompleteSelectMultipleWidget(TagLookup),
        required=False,
    )

    # def clean_owner(self):
    #     value = self.cleaned_data['owner']
    #     if len(value) > 1:
    #         raise forms.ValidationError("You can't select more than 1 owner.")
    #     return value[0]
    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            img = Image.open(image)
            w, h = img.size

            # validate dimensions
            max_width = 500
            max_height = 280
            # if w > max_width or h > max_height:
            #     raise forms.ValidationError(
            #         _('Please use an image that is smaller or equal to '
            #           '%s x %s pixels.' % (max_width, max_height)))
            # print(image.name)
            # validate content type
            fileName, fileExtension = os.path.splitext(image.name)
            print(fileExtension)
            if not fileExtension in ['.jpeg', '.pjpeg', '.png', '.jpg']:
                raise forms.ValidationError(_('Please use a JPEG or PNG image.'))
            # validate file size
            if len(image) > (2 * 1024 * 1024):
                raise forms.ValidationError(_('Image file too large ( maximum 2mb )'))
        # else:
        #     raise forms.ValidationError(_("Couldn't read uploaded image"))
        return image

    class Meta:
        model = CbCategory
        fields =("name","image","description","meta_data","owner","tag","is_visible")


class CbTopicAdminForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(CbTopicAdminForm, self).__init__(*args, **kwargs)
        CATEGORIES = [("", "Select category")]
        for c in CbCategory.objects.only("name"):
            CATEGORIES.append((c.id, c.name))
        self.fields["category"].choices = CATEGORIES

        users = [("", "Select user")]
        # self.fields["owner"] = self.request.user.id
        for c in User.objects.filter(is_superuser=True, is_staff=True, is_active=True):
            users.append((c.id, c.get_full_name()))
        self.fields["owner"].choices = users

    category = forms.Select(choices=[])
    title = forms.CharField(max_length=255, widget=forms.TextInput,label="Title *")
    image = forms.ImageField(required=False,label="Image (max size 2MB, 500 x 280) ")
    description = forms.CharField(widget=forms.Textarea,max_length=1024,label="Description *")
    owner = forms.Select(choices=[])
    meta_data = forms.CharField(required=False,widget=forms.Textarea)
    is_visible = forms.BooleanField(required=False)
    tag = forms.CharField(
            label='Type tag name',
            widget=AutoCompleteSelectMultipleWidget(TagLookup),
            required=False,
         )

    def clean_title(self):

        category = self.cleaned_data.get("category")
        title = self.cleaned_data.get("title")
        if not self.instance.id:
            if CbTopic.objects.filter(category=category.id,title=title):
                raise forms.ValidationError(_("A category cannot have duplicate topic"))
        else:
            if CbTopic.objects.filter(~Q(pk=self.instance.id),category=category.id,title=title):
                raise forms.ValidationError(_("A category cannot have duplicate topic"))
        return title

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            img = Image.open(image)
            w, h = img.size

            # validate dimensions
            max_width = 500
            max_height = 280
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    _('Please use an image that is smaller or equal to '
                      '%s x %s pixels.' % (max_width, max_height)))
            print(image.name)
            # validate content type
            fileName, fileExtension = os.path.splitext(image.name)
            print(fileExtension)
            if not fileExtension in ['.jpeg', '.pjpeg', '.png', '.jpg']:
                raise forms.ValidationError(_('Please use a JPEG or PNG image.'))
            # validate file size
            if len(image) > (2 * 1024 * 1024):
                raise forms.ValidationError(_('Image file too large ( maximum 2mb )'))
        # else:
        #     raise forms.ValidationError(_("Couldn't read uploaded image"))
        return image

    class Meta:
        model = CbTopic
        fields = ("category","title","image","description","owner","tag","is_visible")


class CbTagAdminForm(forms.ModelForm):
    name = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if CbTag.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Tag already exist")
        return name

    class Meta:
        model = CbTag
        fields = ["name"]


class CbQuestionAdminForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        # self.request = kwargs.pop("request")
        super(CbQuestionAdminForm,self).__init__(*args,**kwargs)
        CATEGORIES = [("","Select category")]
        for c in CbCategory.objects.only("name"):
            CATEGORIES.append((c.id,c.name))
        self.fields["category"].choices = CATEGORIES
        self.fields['attached_tags'].widget.attrs['readonly'] = True
        if self.instance.pk:
            tags = []
            for t in self.instance.question_tags.all():
                tags.append(t.tag.name)
            self.fields["attached_tags"].initial = ", ".join(tags)

        users = [("", "Select user")]
        # self.fields["owner"] = self.request.user.id
        for c in User.objects.filter(is_superuser=True, is_staff=True, is_active=True):
            users.append((c.id, c.get_full_name()))
        self.fields["owner"].choices = users

    category = forms.ChoiceField(label="Category *")
    # topic = forms.Select(choices=CbTopic.objects.only("title"))
    topic = AutoCompleteSelectField(
        lookup_class=TopicLookup,
        widget=AutoComboboxSelectWidget,
        label = "Topic *"
    )
    # title = forms.CharField(widget=forms.TextInput,max_length=1024,label="Title *")
    title = forms.CharField(widget=forms.Textarea, max_length=1024,label="Title *")
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 600,"class":"tinymce"}),
                                                            label="Description *")
    owner = forms.Select(choices=[])
    is_deleted = forms.BooleanField(required=False)
    tag = forms.CharField(
        label='Type tag name',
        widget=AutoCompleteSelectMultipleWidget(TagLookup),
        required=False,
    )
    attached_tags = forms.CharField(widget=forms.Textarea,required=False)

    def clean_category(self):
        if not CbCategory.objects.filter(pk = self.cleaned_data.get("category")).exists():
            raise forms.ValidationError("Category does not exist")
            return self.cleaned_data.get("category")
        else:
            return CbCategory.objects.get(pk=self.cleaned_data.get("category"))

    class Meta:
        model = CbQuestion
        fields = ("category","topic","title","description","owner","tag","is_deleted","attached_tags")

    class Media:
        js = ("main/js/admin-question-form-chain-select.js",)


class CbQuestionForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):

        self.request = kwargs.pop("request")
        # cat=0
        # try:
        #     cat = kwargs.get("initial").get("category")
        # except:
        #     pass
        print(args,kwargs)
        # cat = kwargs.get("initial")["category"]
        super(CbQuestionForm,self).__init__(*args,**kwargs)
        CATEGORIES = [("","Select category")]
        # self.fields["owner"] = self.request.user.id
        for c in CbCategory.objects.filter(is_visible=True).only("name"):
            CATEGORIES.append((c.id,c.name))
        self.fields["category"].choices = CATEGORIES

        TOPICS=[("","Select Topics")]
        topics = CbTopic.objects.filter(is_visible=True).only("title")
        for t in topics:
            TOPICS.append((t.id,t.title))
        self.fields["topic"].choices =TOPICS

    category = forms.Select(choices=[])
    topic = forms.ChoiceField(error_messages={'required': 'Please select a topic'})
    # topic = AutoCompleteSelectField(
    #     lookup_class=TopicLookup,
    #     widget=AutoComboboxSelectWidget
    # )
    title = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 600,"class":"tinymce"}))
    owner = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    tag = forms.CharField(widget=forms.HiddenInput(),required=False)
    tag_auto = forms.CharField(widget=forms.TextInput(attrs={"class":"tag_field form-control"}),required=False)
    # tag = forms.CharField(widget=forms.TextInput(attrs={"class":"tag_id"}))
    # tag = forms.CharField(
    #     label='Type tag name',
    #     widget=AutoCompleteSelectMultipleWidget(TagLookup),
    #     required=False,
    # )

    def clean_owner(self):
        return self.request.user

    def clean_category(self):
        if not CbCategory.objects.filter(pk=self.cleaned_data.get("category").id).exists():
            raise forms.ValidationError("Category does not exist")
            return self.cleaned_data.get("category")
        else:
            return self.cleaned_data.get("category")#CbCategory.objects.get(pk=self.cleaned_data.get("category"))

    def clean_topic(self):
            if not CbTopic.objects.filter(pk=self.cleaned_data.get("topic")).exists():
                raise forms.ValidationError("Topic does not exist")
                return self.cleaned_data.get("topic")
            else:
                return CbTopic.objects.get(pk=self.cleaned_data.get("topic"))

    # def save(self, commit=True):
    #     with transaction.atomic():
    #         question = CbQuestion.objects.create(
    #             topic=self.cleaned_data.get("topic"),
    #             category=self.cleaned_data.get("category"),
    #             title=self.cleaned_data.get("title"),
    #             description=self.cleaned_data.get("description"),
    #             owner=self.request.user
    #         )
    #
    #         # if self.cleaned_data.get("tag"):
    #         #     question.question_tags.all().delete()
    #         #     print(self.cleaned_data.get("tag"),"Hellow world")
    #         #     for tag in self.cleaned_data.get("tag"):
    #         #         CbQuestionTag.objects.create(
    #         #             question=question,
    #         #             tag=CbTag.objects.get(pk=tag)
    #         #         )
    #
    #         return question
    # # def save(self, *args, **kwargs):

    class Meta:
        model = CbQuestion
        fields = ("topic","title","description","tag","category","tag_auto","owner")


class ContactForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

