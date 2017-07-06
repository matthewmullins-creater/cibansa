from django import forms
from articles.models import CbArticle
from selectable.forms import AutoCompleteSelectMultipleWidget,AutoComboboxSelectWidget,AutoCompleteSelectField
from main.lookups import TagLookup
from accounts.models import User
from main.models import CbCategory
from tinymce.widgets import TinyMCE
from PIL import Image
import os
from django.utils.translation import ugettext as _


class CbArticleAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop("request")
        super(CbArticleAdminForm, self).__init__(*args, **kwargs)
        CATEGORIES = [("", "Select category")]
        for c in CbCategory.objects.only("name"):
            CATEGORIES.append((c.id, c.name))
        self.fields["category"].choices = CATEGORIES
        self.fields['attached_tags'].widget.attrs['readonly'] = True
        if self.instance.pk:
            tags = []
            for t in self.instance.article_tags.all():
                tags.append(t.tag.name)
            self.fields["attached_tags"].initial = ", ".join(tags)
        users = [("", "Select user")]
        # self.fields["owner"] = self.request.user.id
        for c in User.objects.filter(is_superuser=True, is_staff=True, is_active=True):
            users.append((c.id, c))
        self.fields["user"].choices = users

    title = forms.CharField(label="Title *",max_length=255,widget=forms.TextInput(attrs={"style":"width: 300px;","autocomplete":"off"}))
    # category = forms.Select(choices=CbCategory.objects.only("name"))
    category = forms.ChoiceField(label="Category *")
    image = forms.ImageField(required=False,label="Image (max size 2MB, recommended dimension 1200 x 435) ")
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 600,"class":"tinymce"}),label="Content *")
    # user = forms.Select(choices=User.objects.filter(is_superuser=True,is_staff=True))
    user = forms.Select(choices=[])
    meta_data = forms.CharField(required=False,widget=forms.Textarea(attrs={"class": "mceNoEditor"}))
    is_visible = forms.BooleanField(required=False)
    attached_tags = forms.CharField(widget=forms.Textarea, required=False)
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

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            img = Image.open(image)
            w, h = img.size

            # validate dimensions
            max_width = 1200
            max_height = 435
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
        model = CbArticle
        fields = ("title","category","image","content","user","is_visible","tag","attached_tags")