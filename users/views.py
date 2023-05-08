from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.views.generic import UpdateView
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.models import News
from .forms import ChangeProfile, LoginUserForm, MySetPasswordForm, MySignupForm, RegisterUserForm
from .token import account_activation_token

from allauth.account.views import SignupView

User = get_user_model()


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    template_name = 'registration/password_reset_confirm.html'


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'


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
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(
            request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return redirect("/")
    else:
        return HttpResponse('Activation link is invalid!')


class ChangeProfile(LoginRequiredMixin, UpdateView):
    template_name = 'registration/change_profile.html'
    form_class = ChangeProfile
    success_url = '/'
    model = User


class MySignupView(SignupView):
    template_name = 'registration/signup_google.html'
    form_class = MySignupForm


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    count_posts = News.objects.filter(author=user).count()
    all_posts = News.objects.filter(author=user)
    content = {
        'user': user,
        'count_posts': count_posts,
        'all_posts': all_posts,
    }
    return render(request, 'registration/user_profile.html', context=content)
