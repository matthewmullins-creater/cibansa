from django import forms
from django.contrib.auth import authenticate
from accounts.models import User,CbUserProfile
from django.db import transaction,IntegrityError
from django.utils.translation import gettext_lazy as _
from PIL import Image
import  os


my_default_errors = {
    'required': 'This field is required'
}


class AuthenticationForm(forms.Form):
    """                                                                                                                                  
        Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput,error_messages=my_default_errors)
    password = forms.CharField(widget=forms.widgets.PasswordInput,error_messages=my_default_errors)
    keep_me = forms.CharField(widget=forms.CheckboxInput,required=False)

    class Meta:
        fields = ['email','password',"keep_me"]

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        # if user is None:
        #     raise forms.ValidationError("This account has be deactivated")

        if not user or not user.is_active:
            raise forms.ValidationError("Invalid email or password")

        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    """ Form for registering a new accounts

    """
    email = forms.EmailField(widget=forms.widgets.TextInput,error_messages=my_default_errors)
    first_name = forms.CharField(widget=forms.widgets.TextInput,error_messages=my_default_errors)
    last_name = forms.CharField(widget=forms.widgets.TextInput,error_messages=my_default_errors)
    password = forms.CharField(widget=forms.widgets.PasswordInput,error_messages=my_default_errors)
    phone = forms.IntegerField(widget=forms.widgets.TextInput,error_messages=my_default_errors)


    class Meta:
        model= User
        fields=['email','password']

    def save(self,commit=True,**kwargs):
        with transaction.atomic():
            try:

                user = super(RegistrationForm,self).save(commit=False)
                user.set_password(self.cleaned_data['password'])

                if commit:
                    user.save()
                    user_profile = CbUserProfile.objects.create(
                        first_name=self.cleaned_data['first_name'],
                        last_name=self.cleaned_data['last_name'],
                        phone=self.cleaned_data['phone'],
                        user=user,
                    )
                    user_profile.save()
                    # except:
                    #     pass

                    return user
            except IntegrityError:
                raise forms.ValidationError("Email already exist")


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"First Name *"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Last Name *"}))
    phone = forms.IntegerField(required=False,widget=forms.TextInput(attrs={"class":"form-control",
                                                                         "placeholder":"Phone"}))
    dob = forms.DateField(input_formats=['%Y-%m-%d'],widget=forms.TextInput(attrs={"placeholder":"Date of birth 1990-07-16 *",
                                                                         "class":"form-control"}))
    country = forms.CharField(required=False,widget=forms.TextInput(attrs={"class":"form-control",
                                                                           "placeholder":"Country "}))
    city = forms.CharField(required=False,widget=forms.TextInput(attrs={"class":"form-control",
                                                                        "placeholder":"City"}))
    gender = forms.ChoiceField(choices=[("male","Male"),("female","Female")],
                                                                    widget=forms.Select(attrs={"class":"form-control"}))
    avatar = forms.ImageField(label="Max size = 2MB",required=False)

    has_photo = forms.CharField(widget=forms.TextInput,required=False)

    def clean_avatar(self):
        image = self.cleaned_data.get('avatar', False)

        if image:
            img = Image.open(image)
            w, h = img.size

            # validate dimensions
            # max_width = 500
            # max_height = 280
            # if w > max_width or h > max_height:
            #     raise forms.ValidationError(
            #         _('Please use an image that is smaller or equal to '
            #           '%s x %s pixels.' % (max_width, max_height)))
            # validate content type
            fileName, fileExtension = os.path.splitext(image.name)
            if not fileExtension in ['.jpeg', '.pjpeg', '.png', '.jpg']:
                raise forms.ValidationError(_('Please use a JPEG or PNG image.'))
            # validate file size
            if len(image) > (2 * 1024 * 1024):
                raise forms.ValidationError(_('Image file too large ( maximum 2mb )'))
        # else:
        #     raise forms.ValidationError(_("Couldn't read uploaded image"))
        return image

    class Meta:
        model = CbUserProfile
        fields = ["first_name","last_name","phone","dob","country","city","gender","avatar","has_photo"]


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.widgets.TextInput)

    def clean_email(self):
        try:
            email=self.cleaned_data['email']
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Sorry, this user does not exist.")

        return email


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('New password (confirm)'),
        widget=forms.PasswordInput,
    )

    error_messages = {
        'password_mismatch': _("The two passwords didn't match."),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            User._default_manager.filter(pk=self.user.pk).update(
                password=self.user.password,
            )
        return self.user


