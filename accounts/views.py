from django.shortcuts import render,redirect,get_object_or_404
from accounts.forms import AuthenticationForm,RegistrationForm,ForgotPasswordForm,PasswordResetForm
from django.contrib.auth import authenticate,login as django_login,authenticate,logout as django_logout
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import generic
from django.core.urlresolvers import reverse,reverse_lazy
from accounts.models import CbTempPassword,User
from accounts.util import send_password_reset_token
from django.http import Http404
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
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

                user = authenticate(email=request.POST['email'],password=request.POST['password'])

                if user is not None:
                    if user.is_active:
                        if not is_safe_url(url=redirect_to, host=request.get_host()):
                            redirect_to = "home-page"
                        if not request.POST.get("keep_me"):
                            request.session.set_expiry(0)
                            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE=True

                        django_login(request,user)
                        # if request.POST.get("next"):
                        #     return redirect(request.POST.get("next"))
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

    redirect_to = request.POST.get("next",'home-page')
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = RegistrationForm(data = request.POST)
            if form.is_valid():
                form.save()
                new_user=authenticate(email=form.cleaned_data["email"],password=form.cleaned_data["password"],)
                django_login(request,new_user)
                return redirect(redirect_to)
        else:
            form = RegistrationForm()
        context={
            'form':form
        }

        return render(request,"accounts/signup.html",context)
    else:
        return redirect(redirect_to)


class ForgetPassword(generic.FormView):
    form_class=ForgotPasswordForm
    template_name="accounts/forgot_password.html"

    def get_success_url(self):
        return reverse("reset-sent")

    def get_context_data(self, **kwargs):
        kwargs['url'] = self.request.get_full_path()
        return super(ForgetPassword, self).get_context_data(**kwargs)

    def form_valid(self,form):
        self.user = User.objects.get(email=form.cleaned_data["email"])
        self.temp=CbTempPassword.objects.create(user=self.user)
        send_password_reset_token(self.user,self.request,self.temp)

        return super(ForgetPassword,self).form_valid(form)


def reset_sent(request):
    return render(request,"accounts/reset_sent.html")


def reset_done(request):
    return render(request,"accounts/reset_done.html")


class PasswordReset(generic.FormView):
    template_name="accounts/reset_password.html"
    form_class=PasswordResetForm
    success_url = reverse_lazy("reset_done")

    def invalid(self):
        return self.render_to_response(self.get_context_data(invalid=True))

    def get_form_kwargs(self):
        kwargs = super(PasswordReset, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = None
        self.token= kwargs['token']
        pk = get_object_or_404(CbTempPassword,token=kwargs['token'])

        if pk.used:
            raise Http404

        self.user = get_object_or_404(User, pk=pk.user.id)
        return super(PasswordReset, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        temp = CbTempPassword.objects.get(token=self.token)
        temp.used=True
        temp.save()
        return redirect(self.get_success_url())

@login_required
def logout(request):
    django_logout(request)
    return redirect("/")

