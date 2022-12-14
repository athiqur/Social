from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def clean_password2(self):
        if self.cleaned_data["password"] != self.cleaned_data["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return self.cleaned_data["password2"]
