# Croody Translation Workflow Guide

## Overview

The Croody project uses Django's internationalization (i18n) system with support for 8 languages:
- Spanish (es) - Source language
- English (en)
- French (fr)
- Portuguese (pt)
- Arabic (ar) - RTL support
- Chinese Simplified (zh_Hans)
- Japanese (ja)
- Hindi (hi)

## Translation Status

Current translation coverage (382 total messages):

| Language | Translated | Fuzzy | Untranslated | Progress |
|----------|------------|-------|--------------|----------|
| Spanish (es) | 0 | 0 | 382 | Source |
| English (en) | 72 | 32 | 278 | 19% |
| French (fr) | 34 | 19 | 329 | 9% |
| Portuguese (pt) | 23 | 8 | 351 | 6% |
| Arabic (ar) | 19 | 8 | 355 | 5% + RTL |
| Chinese (zh_Hans) | 19 | 8 | 355 | 5% |
| Japanese (ja) | 19 | 8 | 355 | 5% |
| Hindi (hi) | 19 | 8 | 355 | 5% |

## Translation Workflow

### Phase 1: Automated Translation (Initial Pass)

1. **Rule-based Translation** (Already implemented)
   - Script: `scripts/translate_auto.py`
   - Handles common UI terms
   - Provides quick translations for core terminology

2. **API-based Translation** (Recommended for production)
   - Install: `pip install googletrans==4.0.0rc1` or `deepl`
   - Configure API credentials
   - Run bulk translation for all untranslated messages

3. **Compile Messages**
   ```bash
   export SECRET_KEY="your-secret-key"
   export DJANGO_SETTINGS_MODULE=croody.settings.development
   source .venv/bin/activate
   python manage.py compilemessages
   ```

### Phase 2: Manual Review with Rosetta

**Rosetta** provides a web interface for translation review:

1. **Start the Development Server**
   ```bash
   ./run_dev.sh
   ```

2. **Access Rosetta Interface**
   - URL: http://localhost:8000/rosetta/
   - Select language to translate
   - Review and refine automated translations

3. **Translation Best Practices**
   - Keep translations concise and natural
   - Maintain consistent terminology
   - Consider cultural nuances
   - Test with actual UI context

### Phase 3: Prioritized Translation

**Priority Order:**

1. **English (en)** - Target: 100% (281 messages)
   - Primary international language
   - User's likely second language
   - Foundation for other translations

2. **French (fr)** - Target: 100% (332 messages)
   - European market expansion
   - Cultural relevance

3. **Portuguese (pt)** - Target: 100% (351 messages)
   - Brazil and Portugal markets

4. **Arabic (ar)** - Target: 100% (355 messages)
   - **Special attention**: RTL (Right-to-Left) layout testing
   - Cultural and linguistic nuances

5. **Chinese, Japanese, Hindi** - Target: 100% (355 each)
   - Asian markets expansion

### Phase 4: Quality Assurance

1. **Check for Missing Translations**
   ```bash
   for lang in es en fr pt ar zh_Hans ja hi; do
     echo "=== $lang ==="
     msgfmt --statistics locale/$lang/LC_MESSAGES/django.po
   done
   ```

2. **Test in Browser**
   - Visit http://localhost:8000/
   - Switch languages using the language selector
   - Verify all pages load correctly

3. **RTL Testing (Arabic)**
   - Verify layout reverses correctly
   - Check text alignment and spacing
   - Test navigation flow

4. **Cross-browser Testing**
   - Chrome, Firefox, Safari
   - Mobile browsers
   - Different screen sizes

## Managing Translation Files

### Adding New Translatable Strings

1. **In Templates**
   ```django
   {% load i18n %}
   {% trans "Your text here" %}
   ```

2. **In Python Code**
   ```python
   from django.utils.translation import gettext as _
   _('Your text here')
   ```

3. **Extract Messages**
   ```bash
   python manage.py makemessages --all
   ```

4. **Compile Messages**
   ```bash
   python manage.py compilemessages
   ```

### Translation Scripts

**Automated Translation Script**
```bash
python scripts/translate_auto.py
```

**Translation Statistics**
```bash
# Check individual language
msgfmt --statistics locale/en/LC_MESSAGES/django.po

# Check all languages
for lang in es en fr pt ar zh_Hans ja hi; do
  echo "$lang: $(msgfmt --statistics locale/$lang/LC_MESSAGES/django.po 2>&1)"
done
```

## Technical Details

### URL Structure

- Default language (Spanish): `/` (no prefix)
- Other languages: `/<lang>/` (e.g., `/en/`, `/fr/`)
- Language switch: HTMX-powered smooth transitions
- Auto-detection: Browser language detection with user override

### File Locations

- Translation files: `/locale/<lang>/LC_MESSAGES/django.po`
- Compiled files: `/locale/<lang>/LC_MESSAGES/django.mo`
- Templates: `/templates/`
- Static files: `/static/`

### Key Components

1. **Language Selector**: `/templates/base.html` (lines 150-230)
   - HTMX-powered AJAX requests
   - Smooth visual transitions
   - Smart language detection

2. **Translation Handler**: `static/js/language-selector.js`
   - Browser language detection
   - User preference storage
   - Visual feedback

3. **Django i18n Configuration**
   - Middleware: `django.middleware.locale.LocaleMiddleware`
   - Languages: 8 supported (settings/base.py:169-178)
   - URL patterns: i18n_patterns with prefix_default_language=False

## API Integration for Automated Translation

### Google Translate API

1. **Install**
   ```bash
   pip install googletrans==4.0.0rc1
   ```

2. **Usage Example**
   ```python
   from googletrans import Translator
   translator = Translator()
   result = translator.translate('Hello', dest='es')
   print(result.text)
   ```

3. **Integration**
   - Replace `simple_translate()` in `scripts/translate_auto.py`
   - Add rate limiting (10 requests/second)
   - Implement retry logic for failed requests

### DeepL API

1. **Install**
   ```bash
   pip install deepl
   ```

2. **Usage Example**
   ```python
   import deepl
   translator = deepl.Translator(auth_key)
   result = translator.translate_text('Hello', target_lang='ES')
   print(result.text)
   ```

## Best Practices

1. **Consistency**
   - Use translation memory for repeated terms
   - Maintain glossary of key terms
   - Review translations for consistency

2. **Context**
   - Provide context for translators
   - Use comments in .po files
   - Test translations in UI context

3. **Quality**
   - Native speaker review
   - Cultural appropriateness
   - Technical accuracy

4. **Maintenance**
   - Regular updates
   - Version control for translations
   - Backup translation files

## Troubleshooting

### Common Issues

1. **Translations Not Showing**
   - Check .mo files are compiled
   - Verify Django i18n is enabled
   - Clear browser cache

2. **Language Switching Fails**
   - Check CSRF token in AJAX request
   - Verify set_language URL is accessible
   - Check JavaScript console for errors

3. **Missing Translations**
   - Run `makemessages --all`
   - Ensure templates have `{% load i18n %}`
   - Check for syntax errors in templates

### Debugging Commands

```bash
# Check translation files
python manage.py check --settings=croody.settings.development

# List untranslated messages
msgattrib --untranslated locale/en/LC_MESSAGES/django.po

# Test language detection
python -c "from django.utils.translation import gettext; print(gettext('Hello'))"
```

## Support

For translation issues or questions:
1. Check Django i18n documentation: https://docs.djangoproject.com/en/stable/topics/i18n/
2. Review Rosetta documentation: https://django-rosetta.readthedocs.io/
3. Contact the development team

---

**Last Updated**: December 3, 2024
**Version**: 1.0
**Languages**: 8 (es, en, fr, pt, ar, zh_Hans, ja, hi)
**Total Messages**: 382
