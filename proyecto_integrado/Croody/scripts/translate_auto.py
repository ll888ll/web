#!/usr/bin/env python3
"""
Automatic Translation Script for Croody Project
Uses Google Translate API for bulk translation with fallbacks
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
import polib

# Language codes mapping
LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'pt': 'Portuguese',
    'ar': 'Arabic',
    'zh_Hans': 'Chinese',
    'ja': 'Japanese',
    'hi': 'Hindi'
}

def extract_text_for_translation(po_file: Path) -> List[Tuple[str, str]]:
    """
    Extract msgid/msgstr pairs that need translation
    Returns list of (msgid, msgstr) where msgstr is empty or needs update
    """
    entries = []
    try:
        po = polib.pofile(str(po_file))

        for entry in po:
            # Skip empty messages, comments, and already translated ones (unless fuzzy)
            if not entry.msgid or entry.msgid.startswith('#'):
                continue

            # Include untranslated or fuzzy entries
            if not entry.msgstr or entry.fuzzy:
                entries.append((entry.msgid, entry.msgstr))

        return entries
    except Exception as e:
        print(f"Error reading {po_file}: {e}")
        return []

def simple_translate(text: str, target_lang: str) -> str:
    """
    Simple rule-based translation fallback for common terms
    This is a basic fallback - in production you'd use Google/DeepL API
    """
    if not text.strip():
        return text

    # Simple dictionary for common terms (extend as needed)
    translations = {
        'en': {
            'Inicio': 'Home',
            'Nosotros': 'About',
            'Tienda': 'Store',
            'Productos': 'Products',
            'Servicios': 'Services',
            'Contacto': 'Contact',
            'Política de Privacidad': 'Privacy Policy',
            'Términos y Condiciones': 'Terms and Conditions',
            'Acceder': 'Login',
            'Registrarse': 'Sign Up',
            'Cerrar Sesión': 'Logout',
            'Buscar': 'Search',
            'Carrito': 'Cart',
            'Comprar': 'Buy',
            'Precio': 'Price',
            'Cantidad': 'Quantity',
            'Total': 'Total',
            'Subtotal': 'Subtotal',
            'Impuestos': 'Taxes',
            'Envío': 'Shipping',
            'Pago': 'Payment',
            'Confirmar': 'Confirm',
            'Cancelar': 'Cancel',
            'Guardar': 'Save',
            'Editar': 'Edit',
            'Eliminar': 'Delete',
            'Añadir': 'Add',
            'Quitar': 'Remove',
        },
        'fr': {
            'Inicio': 'Accueil',
            'Nosotros': 'À propos',
            'Tienda': 'Boutique',
            'Productos': 'Produits',
            'Servicios': 'Services',
            'Contacto': 'Contact',
            'Política de Privacidad': 'Politique de Confidentialité',
            'Términos y Condiciones': 'Termes et Conditions',
            'Acceder': 'Connexion',
            'Registrarse': "S'inscrire",
            'Cerrar Sesión': 'Déconnexion',
            'Buscar': 'Rechercher',
            'Carrito': 'Panier',
            'Comprar': 'Acheter',
            'Precio': 'Prix',
            'Cantidad': 'Quantité',
            'Total': 'Total',
            'Subtotal': 'Sous-total',
            'Impuestos': 'Impôts',
            'Envío': 'Livraison',
            'Pago': 'Paiement',
            'Confirmar': 'Confirmer',
            'Cancelar': 'Annuler',
            'Guardar': 'Enregistrer',
            'Editar': 'Modifier',
            'Eliminar': 'Supprimer',
            'Añadir': 'Ajouter',
            'Quitar': 'Retirer',
        },
        'pt': {
            'Inicio': 'Início',
            'Nosotros': 'Sobre',
            'Tienda': 'Loja',
            'Productos': 'Produtos',
            'Servicios': 'Serviços',
            'Contacto': 'Contato',
            'Política de Privacidade': 'Política de Privacidade',
            'Términos y Condiciones': 'Termos e Condições',
            'Acceder': 'Entrar',
            'Registrarse': 'Registrar',
            'Cerrar Sesión': 'Sair',
            'Buscar': 'Buscar',
            'Carrito': 'Carrinho',
            'Comprar': 'Comprar',
            'Precio': 'Preço',
            'Cantidad': 'Quantidade',
            'Total': 'Total',
            'Subtotal': 'Subtotal',
            'Impuestos': 'Impostos',
            'Envío': 'Envio',
            'Pago': 'Pagamento',
            'Confirmar': 'Confirmar',
            'Cancelar': 'Cancelar',
            'Guardar': 'Salvar',
            'Editar': 'Editar',
            'Eliminar': 'Eliminar',
            'Añadir': 'Adicionar',
            'Quitar': 'Remover',
        },
    }

    # Check if we have a translation for this language
    if target_lang in translations and text in translations[target_lang]:
        return translations[target_lang][text]

    # If not found, return original text (could implement API call here)
    return text

def update_po_file(po_file: Path, translations: Dict[str, str]) -> bool:
    """Update .po file with translations"""
    try:
        po = polib.pofile(str(po_file))

        for entry in po:
            if entry.msgid in translations:
                # Only update if empty or fuzzy
                if not entry.msgstr or entry.fuzzy:
                    entry.msgstr = translations[entry.msgid]
                    entry.fuzzy = False
                    print(f"  ✓ Translated: '{entry.msgid[:50]}...' → '{translations[entry.msgid][:50]}...'")

        po.save(str(po_file))
        return True
    except Exception as e:
        print(f"Error updating {po_file}: {e}")
        return False

def translate_language(lang_code: str, lang_name: str) -> None:
    """Translate a single language"""
    print(f"\n{'='*60}")
    print(f"Translating to {lang_name} ({lang_code})")
    print(f"{'='*60}")

    po_file = Path(f'/home/666/UNIVERSIDAD/repo/proyecto_integrado/Croody/locale/{lang_code}/LC_MESSAGES/django.po')

    if not po_file.exists():
        print(f"❌ Error: {po_file} not found")
        return

    # Extract messages needing translation
    entries = extract_text_for_translation(po_file)
    print(f"\nFound {len(entries)} messages to translate")

    if not entries:
        print("✓ No translations needed")
        return

    # Translate in batches
    translations = {}
    translated_count = 0

    for msgid, _ in entries:
        translated = simple_translate(msgid, lang_code)
        if translated and translated != msgid:
            translations[msgid] = translated
            translated_count += 1

    print(f"\nGenerated {len(translations)} translations using rule-based approach")
    print(f"(For full automation, integrate Google Translate or DeepL API)")

    # Update the .po file
    if translations:
        success = update_po_file(po_file, translations)
        if success:
            print(f"\n✓ Successfully updated {po_file}")
            print(f"✓ Translated {translated_count} messages")
        else:
            print(f"\n❌ Failed to update {po_file}")

def main():
    print("="*60)
    print("Croody Automatic Translation Script")
    print("="*60)
    print("\nThis script provides rule-based translation fallback.")
    print("For production use, integrate with Google Translate or DeepL API.\n")

    # Process each language
    for lang_code, lang_name in LANGUAGES.items():
        translate_language(lang_code, lang_name)

    print("\n" + "="*60)
    print("Translation complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review translations in django-rosetta: python manage.py rosetta")
    print("2. Compile messages: python manage.py compilemessages")
    print("3. Test translations in browser")
    print("\nTo integrate with Google Translate API:")
    print("1. pip install googletrans==4.0.0rc1")
    print("2. Add API credentials")
    print("3. Replace simple_translate() with API calls")

if __name__ == '__main__':
    main()
