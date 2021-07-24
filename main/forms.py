from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField()

    def __init__(self, request):
        super().__init__(request.POST)
        if request:
            self.request = request

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            messages.error(self.request, 'passwords don\'t match')
            raise ValidationError('')
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
            messages.error(self.request, 'the same email already exists')
            raise ValidationError('')
        except ObjectDoesNotExist:
            pass
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
            messages.error(self.request, 'the same username already exists')
            raise ValidationError('')
        except ObjectDoesNotExist:
            pass
        super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
