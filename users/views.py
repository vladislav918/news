from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import UpdateView
from .forms import RegisterUserForm, LoginUserForm, ChangeProfile, MySetPasswordForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.http import HttpResponse

User = get_user_model()


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    template_name = 'registration/password_reset_confirm.html'


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': RegisterUserForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('registration/activate_user.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return render(request, 'registration/email_confirm.html')
        return render(request, 'registration/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("/")
    else:
        return HttpResponse('Activation link is invalid!')


class ChangeProfile(UpdateView):
    template_name = 'registration/change_profile.html'
    form_class = ChangeProfile
    success_url = 'change_profile'
    model = User
