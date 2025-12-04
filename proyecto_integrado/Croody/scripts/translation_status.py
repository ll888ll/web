#!/usr/bin/env python3
"""
Translation Status Checker
Shows current translation progress for all languages
"""

import subprocess
import sys
from pathlib import Path

LANGUAGES = [
    ('es', 'Spanish (Source)'),
    ('en', 'English'),
    ('fr', 'French'),
    ('pt', 'Portuguese'),
    ('ar', 'Arabic (RTL)'),
    ('zh_Hans', 'Chinese (Simplified)'),
    ('ja', 'Japanese'),
    ('hi', 'Hindi'),
]

def run_msgfmt_stats(po_file):
    """Run msgfmt --statistics and parse output"""
    try:
        result = subprocess.run(
            ['msgfmt', '--statistics', str(po_file)],
            capture_output=True,
            text=True,
            timeout=5,
            cwd='/home/666/UNIVERSIDAD/repo/proyecto_integrado/Croody'
        )
        # msgfmt outputs to stderr
        output = result.stderr.strip() if result.stderr else result.stdout.strip()
        return output if output else "0 translated, 0 fuzzy, 0 untranslated"
    except Exception as e:
        return f"Error: {e}"

def format_stats(stats_line):
    """Format statistics line for display"""
    if 'translated' in stats_line:
        return stats_line
    elif 'Error' in stats_line:
        return stats_line
    else:
        # No translations or empty file
        return "0 translated, 0 fuzzy, 0 untranslated"

def calculate_percentage(stats_line):
    """Calculate translation percentage"""
    try:
        # Parse "X translated messages, Y fuzzy, Z untranslated"
        parts = stats_line.split(',')
        translated = int(parts[0].split()[0])
        untranslated = int(parts[2].split()[0]) if len(parts) > 2 else 0
        total = translated + untranslated
        if total > 0:
            return (translated / total) * 100
    except:
        pass
    return 0

def main():
    print("=" * 80)
    print(" " * 20 + "CROODY TRANSLATION STATUS")
    print("=" * 80)
    print()

    locale_dir = Path('/home/666/UNIVERSIDAD/repo/proyecto_integrado/Croody/locale')

    total_progress = []
    longest_lang = max(len(name) for _, name in LANGUAGES)

    for lang_code, lang_name in LANGUAGES:
        po_file = locale_dir / lang_code / 'LC_MESSAGES' / 'django.po'

        if not po_file.exists():
            status = "❌ File not found"
            progress = 0
        else:
            stats = run_msgfmt_stats(po_file)
            status = format_stats(stats)
            progress = calculate_percentage(stats)

        total_progress.append(progress)

        # Progress bar
        bar_length = 30
        filled = int(bar_length * progress / 100)
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"{lang_name:>{longest_lang}}: [{bar}] {progress:5.1f}%")
        print(f"{'':>{longest_lang}}  {status}")
        print()

    # Overall progress
    avg_progress = sum(total_progress) / len(total_progress)
    bar_length = 40
    filled = int(bar_length * avg_progress / 100)
    bar = '█' * filled + '░' * (bar_length - filled)

    print("=" * 80)
    print(f"OVERALL PROGRESS: [{bar}] {avg_progress:5.1f}%")
    print("=" * 80)
    print()

    # Next steps
    print("📋 NEXT STEPS:")
    print()
    print("1. Continue manual translation with Rosetta:")
    print("   • Run: ./run_dev.sh")
    print("   • Visit: http://localhost:8000/rosetta/")
    print()
    print("2. Automated translation (install API):")
    print("   • Google: pip install googletrans==4.0.0rc1")
    print("   • DeepL: pip install deepl")
    print("   • Run: python scripts/translate_auto.py")
    print()
    print("3. Check translation quality:")
    print("   • Test all languages in browser")
    print("   • Verify Arabic RTL layout")
    print("   • Test language detection")
    print()
    print("4. Documentation:")
    print("   • Full guide: TRANSLATION_WORKFLOW.md")
    print()

    # Return exit code based on progress
    if avg_progress >= 95:
        print("✅ Translation nearly complete!")
        return 0
    elif avg_progress >= 50:
        print("⚠️  Translation in progress")
        return 1
    else:
        print("❌ Translation needs work")
        return 2

if __name__ == '__main__':
    sys.exit(main())
