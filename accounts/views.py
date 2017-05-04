from django.shortcuts import render,redirect
from accounts.forms import AuthenticationForm,RegistrationForm
from django.contrib.auth import authenticate,login as django_login,authenticate,logout as django_logout
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from accounts.models import CbUserProfile

# Create your views here.



def login(request):
    """
        Login view
    """
    redirect_to = request.POST.get("next",request.GET.get("next", 'home-page'))
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                print(request.POST)
                user = authenticate(email=request.POST['email'],password=request.POST['password'])

                if user is not None:
                    if user.is_active:
                        if not is_safe_url(url=redirect_to, host=request.get_host()):
                            redirect_to = "home-page"
                        if not request.POST.get("keep_me"):
                            request.session.set_expiry(0)
                            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE=True

                        django_login(request,user)
                        return redirect(redirect_to)
            else:
                print(form.errors)
        else:
            form = AuthenticationForm()
        context ={
            "form":form,
            "next":redirect_to
        }
        return render(request,"accounts/login.html",context)
    else:
        return redirect("/")


def register(request):

    """
        Register view
    """
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = RegistrationForm(data = request.POST)
            if form.is_valid():
                form.save()
                new_user=authenticate(email=form.cleaned_data["email"],password=form.cleaned_data["password"],)
                django_login(request,new_user)
                return redirect("home-page")
        else:
            form = RegistrationForm()
        context={
            'form':form
        }

        return render(request,"accounts/signup.html",context)
    else:
        return redirect("/")


@login_required
def logout(request):
    django_logout(request)
    return redirect("/")

