from django import forms
from main.models import CbCategory,CbQuestion,CbTag,CbQuestion,CbTopic,CbTopicTags,CbQuestionTag
from accounts.models import User
from selectable.forms import AutoCompleteSelectMultipleWidget,AutoComboboxSelectWidget,AutoCompleteSelectField
from main.lookups import TagLookup,TopicLookup
from tinymce.widgets import TinyMCE
from  ast import literal_eval
from django.db import transaction


class CbCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=15)
    image = forms.ImageField(required=False)
    description = forms.CharField(max_length=200, required=False,widget=forms.Textarea)
    meta_data = forms.CharField(required=False,widget=forms.Textarea)
    owner = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_superuser=True,is_staff=True))

    def clean_owner(self):
        value = self.cleaned_data['owner']
        if len(value) > 1:
            raise forms.ValidationError("You can't select more than 1 owner.")
        return value[0]

    class Meta:
        model = CbCategory
        fields =("name","image","description","meta_data","owner")


class CbTopicAdminForm(forms.ModelForm):
    title = forms.CharField(max_length=100,widget=forms.TextInput)
    # category = forms.Select(choices=CbCategory.objects.only("name"))
    category = forms.Select(choices=[])
    image = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea)
    # owner = forms.Select(choices=User.objects.filter(is_superuser=True,is_staff=True))
    owner = forms.Select(choices=[])
    meta_data = forms.CharField(required=False,widget=forms.Textarea)
    tag = forms.CharField(
            label='Type tag name',
            widget=AutoCompleteSelectMultipleWidget(TagLookup),
            required=False,
         )

    class Meta:
        model = CbTopic
        fields = ("title","category","image","description","owner","tag")


class CbQuestionAdminForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        # self.request = kwargs.pop("request")
        super(CbQuestionAdminForm,self).__init__(*args,**kwargs)
        # CATEGORIES = [("","Select category")]
        # for c in CbCategory.objects.only("name"):
        #     CATEGORIES.append((c.id,c.name))
        # self.fields["category"].choices = CATEGORIES


    category = forms.ChoiceField()
    # topic = forms.Select(choices=CbTopic.objects.only("title"))
    topic = AutoCompleteSelectField(
        lookup_class=TopicLookup,
        widget=AutoComboboxSelectWidget
    )
    title = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 200}))
    # owner = forms.Select(choices=User.objects.filter(is_superuser=True, is_staff=True))
    owner = forms.Select(choices=[])
    tag = forms.CharField(
        label='Type tag name',
        widget=AutoCompleteSelectMultipleWidget(TagLookup),
        required=False,
    )

    def clean_category(self):
        if not CbCategory.objects.filter(pk = self.cleaned_data.get("category")).exists():
            raise forms.ValidationError("Category does not exist")
            return self.cleaned_data.get("category")
        else:
            return CbCategory.objects.get(pk=self.cleaned_data.get("category"))

    class Meta:
        model = CbQuestion
        fields = ("category","topic","title","description","owner","tag",)


class CbQuestionForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop("request")
        super(CbQuestionForm,self).__init__(*args,**kwargs)
        CATEGORIES = [("","Select category")]
        for c in CbCategory.objects.only("name"):
            CATEGORIES.append((c.id,c.name))
        self.fields["category"].choices = CATEGORIES

    category = forms.ChoiceField()
    # category = forms.Select(choices=CbCategory.objects.only("name"))
    topic = AutoCompleteSelectField(
        lookup_class=TopicLookup,
        widget=AutoComboboxSelectWidget
    )
    title = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 600}))
    # owner = forms.Select(choices=User.objects.filter(is_superuser=True, is_staff=True))
    tag = forms.CharField(
        label='Type tag name',
        widget=AutoCompleteSelectMultipleWidget(TagLookup),
        required=False,
    )

    def clean_category(self):
        if not CbCategory.objects.filter(pk = self.cleaned_data.get("category")).exists():
            raise forms.ValidationError("Category does not exist")
            return self.cleaned_data.get("category")
        else:
            return CbCategory.objects.get(pk=self.cleaned_data.get("category"))

    def save(self, commit=True):
        with transaction.atomic():
            question = CbQuestion.objects.create(
                topic=self.cleaned_data.get("topic"),
                category=self.cleaned_data.get("category"),
                title=self.cleaned_data.get("title"),
                description=self.cleaned_data.get("description"),
                owner=self.request.user
            )

            if self.cleaned_data.get("tag"):
                question.question_tags.all().delete()
                for tag in literal_eval(self.cleaned_data.get("tag")):
                    CbQuestionTag.objects.create(
                        question=question,
                        tag=CbTag.objects.get(pk=tag)
                    )

            return question
    # def save(self, *args, **kwargs):

    class Meta:
        model = CbQuestion
        fields = ("topic","title","description","tag","category")

