from django.views import generic
from user.forms import UserForm, LoginForm
from user.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate
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
            is_active=True
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
    success_url = "/dashboard/"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            print("access", access_token)
            print("refresh", refresh_token)

            response = HttpResponseRedirect(self.success_url)
            response.set_cookie('access', access_token)
            response.set_cookie('refresh', refresh_token)
            return response
        else:
            messages.error(self.request, "Invalid email or password.")
            return self.form_invalid(form)

