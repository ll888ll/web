#!/usr/bin/env python3
"""
Script para expandir traducciones básicas copiando estructura del inglés
Genera archivos .po completos para todos los idiomas basados en el inglés
"""
from pathlib import Path
import re

# Traducciones básicas por idioma usando diccionarios simples
BASIC_TRANSLATIONS = {
    'fr': {
        'Search in Croody': 'Rechercher dans Croody',
        'Login': 'Connexion',
        'Logout': 'Déconnexion',
        'Sign out': 'Se déconnecter',
        'Get Started': 'Commencer',
        'Sign In': 'Se connecter',
        'Skip to main content': 'Passer au contenu principal',
        'Open menu': 'Ouvrir le menu',
        'Select language': 'Sélectionner la langue',
        'Change theme': 'Changer le thème',
        'Quick access': 'Accès rapide',
        'Suggested results': 'Résultats suggérés',
        'Sacred geometry': 'Géométrie sacrée',
        'Legal': 'Légal',
        'Privacy': 'Confidentialité',
        'Terms': 'Conditions',
        'Cookies': 'Cookies',
        "Let's be human again": 'Redevenons humains',
        'Connect your account to continue.': 'Connectez votre compte pour continuer.',
        'Connect, Train and Stand Out': 'Connectez, Entraînez et Démarquez-vous',
    },
    'pt': {
        'Search in Croody': 'Pesquisar no Croody',
        'Login': 'Entrar',
        'Logout': 'Sair',
        'Sign out': 'Sair',
        'Get Started': 'Começar',
        'Sign In': 'Entrar',
        'Skip to main content': 'Pular para o conteúdo principal',
        'Open menu': 'Abrir menu',
        'Select language': 'Selecionar idioma',
        'Change theme': 'Mudar tema',
        'Quick access': 'Acesso rápido',
        'Suggested results': 'Resultados sugeridos',
        'Sacred geometry': 'Geometria sagrada',
        'Legal': 'Legal',
        'Privacy': 'Privacidade',
        'Terms': 'Termos',
        'Cookies': 'Cookies',
        "Let's be human again": 'Vamos ser humanos novamente',
        'Connect your account to continue.': 'Conecte sua conta para continuar.',
        'Connect, Train and Stand Out': 'Conecte, Treine e Destaque-se',
    },
    'ar': {
        'Search in Croody': 'البحث في Croody',
        'Login': 'تسجيل الدخول',
        'Logout': 'تسجيل الخروج',
        'Sign out': 'تسجيل الخروج',
        'Get Started': 'ابدأ',
        'Sign In': 'تسجيل الدخول',
        'Skip to main content': 'انتقل إلى المحتوى الرئيسي',
        'Open menu': 'فتح القائمة',
        'Select language': 'اختر اللغة',
        'Change theme': 'تغيير المظهر',
        'Quick access': 'وصول سريع',
        'Suggested results': 'نتائج مقترحة',
        'Sacred geometry': 'الهندسة المقدسة',
        'Legal': 'قانوني',
        'Privacy': 'الخصوصية',
        'Terms': 'الشروط',
        'Cookies': 'ملفات تعريف الارتباط',
        "Let's be human again": 'لنعد إنسانيين مرة أخرى',
        'Connect your account to continue.': 'اربط حسابك للمتابعة.',
        'Connect, Train and Stand Out': 'اتصل، تدرب وتميز',
    },
    'zh_Hans': {
        'Search in Croody': '在Croody中搜索',
        'Login': '登录',
        'Logout': '登出',
        'Sign out': '退出',
        'Get Started': '开始',
        'Sign In': '登录',
        'Skip to main content': '跳转到主要内容',
        'Open menu': '打开菜单',
        'Select language': '选择语言',
        'Change theme': '更改主题',
        'Quick access': '快速访问',
        'Suggested results': '建议结果',
        'Sacred geometry': '神圣几何',
        'Legal': '法律',
        'Privacy': '隐私',
        'Terms': '条款',
        'Cookies': 'Cookies',
        "Let's be human again": '让我们重新成为人类',
        'Connect your account to continue.': '连接您的帐户以继续。',
        'Connect, Train and Stand Out': '连接、训练和脱颖而出',
    },
    'ja': {
        'Search in Croody': 'Croo dyで検索',
        'Login': 'ログイン',
        'Logout': 'ログアウト',
        'Sign out': 'サインアウト',
        'Get Started': '始める',
        'Sign In': 'サインイン',
        'Skip to main content': 'メインコンテンツへスキップ',
        'Open menu': 'メニューを開く',
        'Select language': '言語を選択',
        'Change theme': 'テーマを変更',
        'Quick access': 'クイックアクセス',
        'Suggested results': '提案された結果',
        'Sacred geometry': '神聖幾何学',
        'Legal': '法的',
        'Privacy': 'プライバシー',
        'Terms': '利用規約',
        'Cookies': 'クッキー',
        "Let's be human again": 'もう一度人間になろう',
        'Connect your account to continue.': 'アカウントを接続して続行してください。',
        'Connect, Train and Stand Out': '接続、トレーニング、目立つ',
    },
    'hi': {
        'Search in Croody': 'Croody में खोजें',
        'Login': 'लॉग इन करें',
        'Logout': 'लॉग आउट',
        'Sign out': 'साइन आउट',
        'Get Started': 'शुरू करें',
        'Sign In': 'साइन इन करें',
        'Skip to main content': 'मुख्य सामग्री पर जाएं',
        'Open menu': 'मेनू खोलें',
        'Select language': 'भाषा चुनें',
        'Change theme': 'थीम बदलें',
        'Quick access': 'त्वरित पहुंच',
        'Suggested results': 'सुझाए गए परिणाम',
        'Sacred geometry': 'पवित्र ज्यामिति',
        'Legal': 'कानूनी',
        'Privacy': 'गोपनीयता',
        'Terms': 'शर्तें',
        'Cookies': 'कुकीज़',
        "Let's be human again": 'आइए फिर से इंसान बनें',
        'Connect your account to continue.': 'जारी रखने के लिए अपना खाता कनेक्ट करें।',
        'Connect, Train and Stand Out': 'कनेक्ट करें, प्रशिक्षण लें और अलग दिखें',
    },
}

def parse_en_po():
    """Parse archivo inglés y extraer todas las traducciones"""
    en_po = Path('locale/en/LC_MESSAGES/django.po')
    
    with open(en_po, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer header
    header_match = re.search(r'msgid ""\nmsgstr ""(.*?)(?=\n\n|\nmsgid)', content, re.DOTALL)
    header = header_match.group(1) if header_match else ''
    
    # Extraer pares msgid/msgstr
    entries = []
    pattern = r'msgid "((?:[^"\\]|\\.)*)"\nmsgstr "((?:[^"\\]|\\.)*)"'
    
    for match in re.finditer(pattern, content):
        msgid = match.group(1)
        msgstr = match.group(2)
        if msgid:  # Skip header
            entries.append((msgid, msgstr))
    
    return header, entries

def create_translation_file(lang_code, header, entries, translations):
    """Crea archivo .po para un idioma con traducciones"""
    lang_name = {
        'fr': 'French',
        'pt': 'Portuguese', 
        'ar': 'Arabic',
        'zh_Hans': 'Chinese Simplified',
        'ja': 'Japanese',
        'hi': 'Hindi'
    }[lang_code]
    
    # Actualizar header
    header = header.replace('English', lang_name)
    header = header.replace('Language: en', f'Language: {lang_code}')
    
    # Escribir archivo
    output = f'locale/{lang_code}/LC_MESSAGES/django.po'
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(f'# {lang_name} translations for Croody project.\n')
        f.write('# Copyright (C) 2024 Croody\n')
        f.write('#\n')
        f.write('msgid ""\n')
        f.write('msgstr ""\n')
        f.write(header)
        f.write('\n')
        
        for msgid, msgstr_en in entries:
            # Usar traducción si existe, sino dejar msgstr vacío (fallback a español)
            msgstr_target = translations.get(msgstr_en, '')
            
            f.write(f'msgid "{msgid}"\n')
            f.write(f'msgstr "{msgstr_target}"\n')
            f.write('\n')
    
    print(f'✓ Created: {output}')
    print(f'  {len([t for t in translations.values() if t])} translations, {len(entries) - len([t for t in translations.values() if t])} fallbacks')

def main():
    print('Expanding translations from English...')
    print()
    
    header, entries = parse_en_po()
    print(f'Found {len(entries)} entries in English')
    print()
    
    for lang_code, translations in BASIC_TRANSLATIONS.items():
        create_translation_file(lang_code, header, entries, translations)
    
    print()
    print('✅ All translation files updated!')
    print('Run: python3 compile_translations.py')

if __name__ == '__main__':
    main()
