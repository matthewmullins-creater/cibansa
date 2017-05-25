from django import forms
from django.contrib.auth import authenticate
from accounts.models import User,CbUserProfile
from django.db import transaction,IntegrityError
from django.utils.translation import ugettext_lazy as _


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
    phone = forms.CharField(widget=forms.widgets.TextInput,error_messages=my_default_errors)


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


