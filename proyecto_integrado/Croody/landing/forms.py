"""Formularios personalizados para el módulo landing."""
from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import UserProfile

User = get_user_model()


class CroodyLoginForm(AuthenticationForm):
    """Formulario de login con estilos personalizados de Croody."""

    username = forms.CharField(
        label=_('Usuario o correo'),
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'auth-input',
                'placeholder': 'ej. mateo@croody.app',
                'autocomplete': 'username',
            }
        ),
    )

    password = forms.CharField(
        label=_('Contraseña'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'auth-input',
                'placeholder': '••••••••',
                'autocomplete': 'current-password',
            }
        ),
    )

    def clean(self):  # type: ignore[override]
        username = self.cleaned_data.get('username')
        if username and '@' in username:
            try:
                user = User.objects.get(email__iexact=username)
                self.cleaned_data['username'] = user.get_username()
            except User.DoesNotExist:
                pass
        return super().clean()


class CroodySignupForm(UserCreationForm):
    full_name = forms.CharField(
        label=_('Nombre completo'),
        max_length=160,
        widget=forms.TextInput(
            attrs={
                'class': 'auth-input',
                'placeholder': _('Nombre y apellidos'),
                'autocomplete': 'name',
            }
        ),
    )
    email = forms.EmailField(
        label=_('Correo electrónico'),
        widget=forms.EmailInput(
            attrs={'class': 'auth-input', 'placeholder': 'tucorreo@croody.app', 'autocomplete': 'email'}
        ),
    )
    preferred_language = forms.ChoiceField(
        label=_('Idioma preferido'),
        choices=[('es', 'Español'), ('en', 'English'), ('fr', 'Français'), ('pt', 'Português')],
        widget=forms.Select(attrs={'class': 'auth-input'}),
    )
    preferred_theme = forms.ChoiceField(
        label=_('Tema visual'),
        choices=UserProfile.THEME_CHOICES,
        widget=forms.Select(attrs={'class': 'auth-input'}),
    )
    accept_terms = forms.BooleanField(label=_('Acepto el manifiesto Croody y términos de servicio'))

    class Meta(UserCreationForm.Meta):  # type: ignore[misc]
        model = User
        fields = ('full_name', 'email', 'preferred_language', 'preferred_theme', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('Ya existe una cuenta con este correo.'))
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('password1', 'password2'):
            self.fields[name].widget.attrs.update({'class': 'auth-input'})
        self.fields['accept_terms'].widget.attrs.update({'class': 'auth-checkbox'})

    def _build_username(self, email: str) -> str:
        base = email.split('@')[0][:30] or 'croody'
        candidate = base
        idx = 1
        while User.objects.filter(username=candidate).exists():
            candidate = f"{base}-{idx}"
            idx += 1
        return candidate

    def save(self, commit: bool = True):  # type: ignore[override]
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        user.email = email
        user.username = self._build_username(email)
        full_name = self.cleaned_data['full_name'].strip()
        if full_name:
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
        if commit:
            user.save()
            profile = user.profile  # type: ignore[attr-defined]
            profile.preferred_language = self.cleaned_data['preferred_language']
            profile.preferred_theme = self.cleaned_data['preferred_theme']
            profile.display_name = full_name or user.username
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': _('Nombre')}),
            'last_name': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': _('Apellidos')}),
            'email': forms.EmailInput(attrs={'class': 'auth-input', 'placeholder': 'tucorreo@croody.app'}),
        }


class ProfilePreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'display_name',
            'preferred_language',
            'preferred_theme',
            'timezone',
            'notification_level',
            'telemetry_alerts',
            'favorite_robot',
            'bio',
        )
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'auth-input'}),
            'timezone': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'UTC'}),
            'notification_level': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'smart'}),
            'favorite_robot': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'robot-alpha'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'auth-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'auth-checkbox'})
            else:
                field.widget.attrs.setdefault('class', 'auth-input')


class TokenResetForm(forms.Form):
    confirm = forms.BooleanField(widget=forms.HiddenInput, initial=True)
