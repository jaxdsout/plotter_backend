from django import forms


class ProfileForm(forms.Form):
    trec = forms.CharField(max_length=6)
    website = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20)
    avatar = forms.ImageField(required=False)

