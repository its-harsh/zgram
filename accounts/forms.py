from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput,
        validators=[password_validation.validate_password, ],
        help_text=password_validation.password_validators_help_text_html()
    )
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,
                                       help_text='Enter same password as above to verify you typed correctly.')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password == confirm_password:
            return confirm_password
        else:
            raise forms.ValidationError(
                message='Two password field does\'nt match.', code='password-mismatch'
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs = {
                'autofous': True}

    def save(self, commit):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label='Password', help_text='Raw passwords are not stored, so there is no way to see this '
        'user’s password, but you can change the password using '
        '<a href="../password/">this form</a>.'
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial.get('password')

    def clean_is_superuser(self):
        is_superuser = self.cleaned_data.get('is_superuser')
        if is_superuser:
            self.cleaned_data['is_staff'] = True
            self.cleaned_data['is_active'] = True
        return is_superuser
