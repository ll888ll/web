"""Formularios del ecosistema post-login de Croody."""
from __future__ import annotations

import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import UserProfile, Gender


class ProfileEditForm(forms.ModelForm):
    """Formulario para editar el perfil del usuario."""

    class Meta:
        model = UserProfile
        fields = [
            'profile_picture',
            'weight',
            'height',
            'birth_date',
            'gender',
            'bio',
            'fitness_goals',
        ]
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-input',
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'form-textarea',
                    'placeholder': _('Cuéntanos sobre ti...'),
                }
            ),
            'weight': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': _('Ej: 70.5'),
                    'step': '0.1',
                    'min': '20',
                    'max': '300',
                }
            ),
            'height': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': _('Ej: 175'),
                    'step': '0.1',
                    'min': '100',
                    'max': '250',
                }
            ),
            'profile_picture': forms.FileInput(
                attrs={
                    'class': 'form-file',
                    'accept': 'image/*',
                }
            ),
        }

    def clean_weight(self):
        """Validar peso."""
        weight = self.cleaned_data.get('weight')
        if weight is not None:
            if weight < 20 or weight > 300:
                raise ValidationError(_('El peso debe estar entre 20 y 300 kg.'))
        return weight

    def clean_height(self):
        """Validar altura."""
        height = self.cleaned_data.get('height')
        if height is not None:
            if height < 100 or height > 250:
                raise ValidationError(_('La altura debe estar entre 100 y 250 cm.'))
        return height

    def clean_profile_picture(self):
        """Validar imagen de perfil."""
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Verificar tamaño (máximo 5MB)
            if picture.size > 5 * 1024 * 1024:
                raise ValidationError(_('La imagen no puede superar 5MB.'))

            # Verificar tipo de archivo
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if hasattr(picture, 'content_type') and picture.content_type not in allowed_types:
                raise ValidationError(_('Solo se permiten imágenes JPEG, PNG, GIF o WebP.'))

        return picture


class WalletConnectForm(forms.ModelForm):
    """Formulario para conectar wallet Solana."""

    class Meta:
        model = UserProfile
        fields = ['solana_public_key']
        widgets = {
            'solana_public_key': forms.TextInput(
                attrs={
                    'class': 'form-input font-mono',
                    'placeholder': _('Tu llave pública de Solana...'),
                    'maxlength': '44',
                }
            ),
        }

    def clean_solana_public_key(self):
        """Validar formato de llave pública Solana."""
        key = self.cleaned_data.get('solana_public_key', '').strip()

        if not key:
            return key

        # Validar longitud (32-44 caracteres en base58)
        if len(key) < 32 or len(key) > 44:
            raise ValidationError(
                _('La llave pública debe tener entre 32 y 44 caracteres.')
            )

        # Validar caracteres base58 (sin 0, O, I, l)
        base58_pattern = r'^[1-9A-HJ-NP-Za-km-z]+$'
        if not re.match(base58_pattern, key):
            raise ValidationError(
                _('La llave pública contiene caracteres inválidos.')
            )

        return key


class TransactionSubmitForm(forms.Form):
    """Formulario para enviar una transacción para verificación."""

    tx_signature = forms.CharField(
        label=_('Firma de transacción'),
        max_length=88,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input font-mono',
                'placeholder': _('Pega aquí la firma de tu transacción...'),
            }
        ),
        help_text=_('La firma de la transacción de Solana (88 caracteres).')
    )

    def clean_tx_signature(self):
        """Validar formato de firma de transacción."""
        sig = self.cleaned_data.get('tx_signature', '').strip()

        if not sig:
            raise ValidationError(_('La firma de transacción es requerida.'))

        # Validar longitud (88 caracteres en base58)
        if len(sig) != 88:
            raise ValidationError(
                _('La firma debe tener exactamente 88 caracteres.')
            )

        # Validar caracteres base58
        base58_pattern = r'^[1-9A-HJ-NP-Za-km-z]+$'
        if not re.match(base58_pattern, sig):
            raise ValidationError(
                _('La firma contiene caracteres inválidos.')
            )

        return sig


class FitnessGoalsForm(forms.Form):
    """Formulario para objetivos de fitness."""

    GOAL_CHOICES = [
        ('weight_loss', _('Perder peso')),
        ('muscle_gain', _('Ganar músculo')),
        ('endurance', _('Mejorar resistencia')),
        ('flexibility', _('Mejorar flexibilidad')),
        ('general_health', _('Salud general')),
        ('stress_relief', _('Reducir estrés')),
        ('better_sleep', _('Mejorar sueño')),
    ]

    goals = forms.MultipleChoiceField(
        label=_('Objetivos de fitness'),
        choices=GOAL_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-checkbox',
            }
        ),
        required=False,
    )
