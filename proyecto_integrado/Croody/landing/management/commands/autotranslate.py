"""
Auto-translate Django .po files using Google Translate.

Usage:
    python manage.py autotranslate
    python manage.py autotranslate --lang=fr
    python manage.py autotranslate --force  # Re-translate all, not just empty

This command automatically translates all untranslated strings in .po files
from Spanish (source) to all configured languages.
"""

import os
import time
from pathlib import Path

import polib
from deep_translator import GoogleTranslator
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Auto-translate .po files from Spanish to other languages"

    # Map Django locale codes to Google Translate codes
    LANG_MAP = {
        "en": "en",
        "fr": "fr",
        "pt": "pt",
        "ar": "ar",
        "zh_Hans": "zh-CN",
        "ja": "ja",
        "hi": "hi",
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--lang",
            type=str,
            help="Translate only this language (e.g., 'en', 'fr')",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force re-translation of all strings, not just empty ones",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be translated without making changes",
        )

    def handle(self, *args, **options):
        locale_path = Path(settings.BASE_DIR) / "locale"
        target_lang = options.get("lang")
        force = options.get("force", False)
        dry_run = options.get("dry_run", False)

        if target_lang:
            languages = [target_lang] if target_lang in self.LANG_MAP else []
            if not languages:
                self.stderr.write(
                    self.style.ERROR(f"Unknown language: {target_lang}")
                )
                return
        else:
            languages = list(self.LANG_MAP.keys())

        for lang in languages:
            po_path = locale_path / lang / "LC_MESSAGES" / "django.po"
            if not po_path.exists():
                self.stderr.write(
                    self.style.WARNING(f"File not found: {po_path}")
                )
                continue

            self.stdout.write(f"\n{'=' * 50}")
            self.stdout.write(
                self.style.SUCCESS(f"Processing {lang.upper()}...")
            )
            self.translate_file(po_path, lang, force, dry_run)

        if not dry_run:
            self.stdout.write("\n" + "=" * 50)
            self.stdout.write(
                self.style.SUCCESS(
                    "Done! Run 'python manage.py compilemessages' to compile."
                )
            )

    def translate_file(self, po_path, lang, force, dry_run):
        """Translate a single .po file."""
        po = polib.pofile(str(po_path))
        google_lang = self.LANG_MAP.get(lang, lang)

        # Get entries to translate
        if force:
            entries = [e for e in po if e.msgid and not e.obsolete]
        else:
            entries = po.untranslated_entries() + [
                e for e in po if e.fuzzy and not e.obsolete
            ]

        if not entries:
            self.stdout.write(f"  No untranslated entries for {lang}")
            return

        self.stdout.write(f"  Found {len(entries)} entries to translate")

        translator = GoogleTranslator(source="es", target=google_lang)
        translated_count = 0
        errors = 0

        for i, entry in enumerate(entries):
            if not entry.msgid or entry.msgid == "":
                continue

            try:
                # Handle multiline strings
                text = entry.msgid
                if "\n" in text:
                    # Translate line by line for multiline
                    lines = text.split("\n")
                    translated_lines = []
                    for line in lines:
                        if line.strip():
                            translated_lines.append(
                                translator.translate(line)
                            )
                        else:
                            translated_lines.append(line)
                    translated = "\n".join(translated_lines)
                else:
                    translated = translator.translate(text)

                if translated:
                    if dry_run:
                        self.stdout.write(
                            f"  [{i + 1}/{len(entries)}] "
                            f"'{text[:50]}...' -> '{translated[:50]}...'"
                        )
                    else:
                        entry.msgstr = translated
                        # Remove fuzzy flag if present
                        if "fuzzy" in entry.flags:
                            entry.flags.remove("fuzzy")
                    translated_count += 1

                # Rate limiting to avoid API blocks
                if (i + 1) % 10 == 0:
                    time.sleep(0.5)

            except Exception as e:
                errors += 1
                self.stderr.write(
                    self.style.WARNING(
                        f"  Error translating '{entry.msgid[:30]}...': {e}"
                    )
                )
                # Longer pause on error
                time.sleep(1)

            # Progress indicator
            if (i + 1) % 50 == 0:
                self.stdout.write(
                    f"  Progress: {i + 1}/{len(entries)} "
                    f"({translated_count} translated, {errors} errors)"
                )

        if not dry_run:
            po.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"  Completed: {translated_count} translated, {errors} errors"
            )
        )
