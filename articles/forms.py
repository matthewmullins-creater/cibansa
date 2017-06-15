from django import forms
from articles.models import CbArticle
from selectable.forms import AutoCompleteSelectMultipleWidget,AutoComboboxSelectWidget,AutoCompleteSelectField
from main.lookups import TagLookup
from accounts.models import User
from main.models import CbCategory
from tinymce.widgets import TinyMCE


class CbArticleAdminForm(forms.ModelForm):
    title = forms.CharField(label="Title *",max_length=255,widget=forms.TextInput(attrs={"style":"width: 300px;","autocomplete":"off"}))
    category = forms.Select(choices=CbCategory.objects.only("name"))
    image = forms.ImageField(required=False)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 600,"class":"tinymce"}),label="Content *")
    user = forms.Select(choices=User.objects.filter(is_superuser=True,is_staff=True))
    meta_data = forms.CharField(required=False,widget=forms.Textarea(attrs={"class": "mceNoEditor"}))
    is_visible = forms.BooleanField(required=False)
    tag = forms.CharField(
            label='Type tag name',
            widget=AutoCompleteSelectMultipleWidget(TagLookup),
            required=False,
         )

    class Meta:
        model = CbArticle
        fields = ("title","category","image","content","user","tag","is_visible")