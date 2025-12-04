"""Formularios y helpers para la tienda."""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List

from django import forms
from django.contrib.auth.models import User


class Cart:
    """Helper para gestionar el carrito en la sesión."""
    
    CART_SESSION_KEY = 'cart'
    
    def __init__(self, request: Any) -> None:
        """Inicializar carrito desde la sesión."""
        self.session = request.session
        cart = self.session.get(self.CART_SESSION_KEY)
        if not cart:
            cart = self.session[self.CART_SESSION_KEY] = {}
        self.cart = cart
    
    def add(
        self,
        product_id: int,
        quantity: int = 1,
        override_quantity: bool = False
    ) -> None:
        """Agregar producto al carrito."""
        product_id = str(product_id)
        
        if product_id in self.cart:
            if override_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'quantity': quantity,
            }
        
        self.save()
    
    def remove(self, product_id: int) -> None:
        """Remover producto del carrito."""
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def update_quantity(self, product_id: int, quantity: int) -> None:
        """Actualizar cantidad de un producto."""
        if quantity <= 0:
            self.remove(product_id)
        else:
            self.add(product_id, quantity, override_quantity=True)
    
    def save(self) -> None:
        """Guardar carrito en la sesión."""
        self.session.modified = True
    
    def clear(self) -> None:
        """Limpiar carrito."""
        del self.session[self.CART_SESSION_KEY]
        self.session.modified = True
    
    def get_total_price(self) -> Decimal:
        """Calcular precio total del carrito."""
        from .models import Product
        
        total = Decimal('0.00')
        for product_id, item_data in self.cart.items():
            try:
                product = Product.objects.get(id=product_id, is_published=True)
                total += product.price * item_data['quantity']
            except Product.DoesNotExist:
                continue
        return total
    
    def get_item_count(self) -> int:
        """Contar items en el carrito."""
        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        """Iterar sobre items del carrito."""
        from .models import Product
        
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids, is_published=True)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item_data in cart.values():
            item_data['total_price'] = item_data['product'].price * item_data['quantity']
            yield item_data
    
    def __len__(self) -> int:
        """Número total de items en el carrito."""
        return sum(item['quantity'] for item in self.cart.values())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir carrito a diccionario para serialización."""
        return self.cart


class CheckoutForm(forms.Form):
    """Formulario para datos de checkout."""
    
    # Datos personales
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Apellidos'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '+34 600 000 000'
        })
    )
    
    # Dirección
    address_line_1 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Calle, número'
        })
    )
    address_line_2 = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Apartamento, suite, etc. (opcional)'
        })
    )
    city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Ciudad'
        })
    )
    state = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Provincia/Estado'
        })
    )
    postal_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Código postal'
        })
    )
    country = forms.CharField(
        max_length=50,
        initial='España',
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'País'
        })
    )
    
    # Método de pago
    payment_method = forms.ChoiceField(
        choices=[
            ('stripe', 'Tarjeta de crédito/débito'),
            ('paypal', 'PayPal'),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'radio-list'
        })
    )
    
    # Notas adicionales
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea',
            'rows': 4,
            'placeholder': 'Notas adicionales sobre tu pedido (opcional)'
        })
    )
    
    def clean(self) -> Dict[str, Any]:
        """Validaciones adicionales."""
        cleaned_data = super().clean()
        
        # Validar que el email sea correcto
        email = cleaned_data.get('email')
        if email:
            # Verificar si el usuario existe
            if User.objects.filter(email=email).exists():
                # Opcional: asociar con usuario existente
                pass
        
        return cleaned_data


class PaymentForm(forms.Form):
    """Formulario para datos de pago (simulado)."""
    
    card_number = forms.CharField(
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '1234 5678 9012 3456',
            'autocomplete': 'cc-number'
        })
    )
    expiry_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'MM/YY',
            'autocomplete': 'cc-exp'
        })
    )
    cvv = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '123',
            'autocomplete': 'cc-csc'
        })
    )
    cardholder_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Nombre del titular',
            'autocomplete': 'cc-name'
        })
    )
    
    def clean_card_number(self) -> str:
        """Validar número de tarjeta."""
        card_number = self.cleaned_data['card_number'].replace(' ', '')
        if not card_number.isdigit():
            raise forms.ValidationError('El número de tarjeta debe contener solo dígitos.')
        if len(card_number) < 13 or len(card_number) > 19:
            raise forms.ValidationError('Número de tarjeta inválido.')
        return card_number
    
    def clean_expiry_date(self) -> str:
        """Validar fecha de expiración."""
        expiry = self.cleaned_data['expiry_date']
        if '/' not in expiry:
            raise forms.ValidationError('Formato debe ser MM/YY.')
        try:
            month, year = expiry.split('/')
            month = int(month)
            year = int(year)
            if month < 1 or month > 12:
                raise forms.ValidationError('Mes inválido.')
        except ValueError:
            raise forms.ValidationError('Formato de fecha inválido.')
        return expiry
    
    def clean_cvv(self) -> str:
        """Validar CVV."""
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            raise forms.ValidationError('CVV inválido.')
        return cvv
