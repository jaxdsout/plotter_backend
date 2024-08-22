import requests
from user.forms import UserForm, LoginForm
from user.models import User
from agent.forms import ProfileForm
from agent.models import Profile

from django.views import generic
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect


class HomePage(generic.TemplateView):
    template_name = "home.html"


class Dashboard(generic.TemplateView):
    template_name = "dashboard.html"


class UserRegister(generic.FormView):
    template_name = "user_register.html"
    form_class = UserForm
    success_url = "/"

    def form_valid(self, form):
        user = User.objects.create_user(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        user.save()

        return redirect(self.success_url)


class UserVerify(generic.TemplateView):
    template_name = "user_verify.html"

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('uid')
        token = kwargs.get('token')
        user = get_object_or_404(User, pk=user_id)

        if default_token_generator.check_token(user, token):
            self.set_active(user)
            messages.success(request, 'Your account has been activated successfully.')
            return redirect(reverse('user_login'))
        else:
            messages.error(request, 'The activation link is invalid or has expired.')
            return redirect(reverse('user_signup'))

    def set_active(self, user):
        user.is_active = True
        user.save()


class UserLogin(generic.FormView):
    template_name = "user_login.html"
    form_class = LoginForm
    success_url = "/user/dashboard/"

    def form_valid(self, form):
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])

        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            id_token = str(user.id)

            response = HttpResponseRedirect(self.success_url)
            response.set_cookie('access', access_token)
            response.set_cookie('refresh', refresh_token)
            response.set_cookie('id', id_token)

            return response

        else:
            messages.error(self.request, "Please enter valid email & password")
            return self.form_invalid(form)


class UserLogout(generic.RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        refresh_token = request.COOKIES.get('refresh')

        if access_token:
            try:
                token = RefreshToken(access_token)
                token.blacklist()
            except Exception as e:
                print(f"Error blacklisting token: {e}")

        response = HttpResponseRedirect(self.url)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        logout(request)

        return response


class UserProfile(generic.FormView):
    template_name = "user_profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy('user_profile')

    def form_valid(self, form, request):
        profile = form.save(commit=False)
        id_token = self.request.COOKIES.get('id')
        profile.user = id_token
        profile.save()
        access_token = self.request.COOKIES.get('access')
        if access_token and id_token:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get('http://localhost:8000/api/profiles/', headers=headers)
            data = response.json()
        return super().form_valid(form)


