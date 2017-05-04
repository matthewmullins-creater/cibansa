from django import forms
from django.contrib.auth import authenticate
from accounts.models import User,CbUserProfile
from django.db import transaction,IntegrityError


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

