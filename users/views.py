from django.contrib.auth.views import LoginView
from django.contrib.auth import login, get_user_model, authenticate
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import UpdateView
from .forms import RegisterUserForm, LoginUserForm, ChangeProfile

User = get_user_model()


# Create your views here.

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
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class ChangeProfile(UpdateView):
    template_name = 'registration/change_profile.html'
    form_class = ChangeProfile
    success_url = '/'
    model = User
