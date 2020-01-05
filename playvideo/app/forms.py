from django import forms
from app.models import UserModel, VideoDetailModel
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'au-input au-input--full', 'placeholder': 'Password'})
    )

    class Meta:
        model = UserModel
        fields = ('email', 'full_name')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'au-input au-input--full', 'placeholder': 'Email'}),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserModel
        fields = ('email', 'password', 'full_name', 'is_active', 'is_admin')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'disabled': True}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class VideoDetailForm(forms.ModelForm):
    class Meta:
        model = VideoDetailModel
        fields = ("video", "title", "description", "categories", "tags", "thumbnail")
        widgets = {
            'video': forms.FileInput(attrs={'accept': 'video/*', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'thumbnail'}),
        }
