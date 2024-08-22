from django import forms


class UserForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")

        if password and re_password and password != re_password:
            self.add_error('password_confirmation', "Passwords do not match.")


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

