#!/usr/bin/env python3
"""
Script para compilar traducciones manualmente sin gettext
Convierte archivos .po a .mo usando Python puro
"""
import os
import struct
from pathlib import Path

def compile_po_file(po_path, mo_path):
    """Compila un archivo .po a .mo con soporte UTF-8 completo"""
    translations = {}
    current_msgid = None
    current_msgstr = None
    header_msgstr = []
    reading_header_msgstr = False
    
    with open(po_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            if line.startswith('msgid "'):
                if current_msgid is not None and current_msgstr is not None:
                    translations[current_msgid] = current_msgstr
                current_msgid = line[7:-1]  # Remove 'msgid "' and '"'
                current_msgstr = None
                reading_header_msgstr = False
                
            elif line.startswith('msgstr "'):
                current_msgstr = line[8:-1]  # Remove 'msgstr "' and '"'
                if current_msgid == '':
                    reading_header_msgstr = True
                    header_msgstr.append(current_msgstr)
                
            elif line.startswith('"') and current_msgstr is not None:
                # Continuation line
                content = line[1:-1]
                current_msgstr += content
                if reading_header_msgstr:
                    header_msgstr.append(content)
    
    # Add last translation
    if current_msgid is not None and current_msgstr is not None:
        translations[current_msgid] = current_msgstr
    
    # Ensure proper UTF-8 header exists
    # CRITICAL: Force UTF-8 in header regardless of .po content
    if '' in translations:
        # If header exists, ensure it has charset=UTF-8
        if 'charset=' not in translations[''].lower():
            translations[''] += 'Content-Type: text/plain; charset=UTF-8\\n'
        elif 'charset=utf-8' not in translations[''].lower():
            # Replace charset with UTF-8
            import re
            translations[''] = re.sub(
                r'charset=[^\n\\]+',
                'charset=UTF-8',
                translations[''],
                flags=re.IGNORECASE
            )
    else:
        # Create minimal header
        translations[''] = 'Content-Type: text/plain; charset=UTF-8\\n'
        print(f"  Created UTF-8 header")
    
    # Build .mo file with proper encoding
    keys = sorted(translations.keys())
    offsets = []
    ids = b''
    strs = b''
    
    for key in keys:
        key_bytes = key.encode('utf-8')
        str_bytes = translations[key].encode('utf-8')
        
        offsets.append((len(ids), len(key_bytes), len(strs), len(str_bytes)))
        ids += key_bytes + b'\x00'
        strs += str_bytes + b'\x00'
    
    # MO file header
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    
    # Write .mo file with little-endian format
    with open(mo_path, 'wb') as f:
        # Magic number (little-endian: 0x950412de)
        f.write(struct.pack('<I', 0x950412de))
        # Version (0)
        f.write(struct.pack('<I', 0))
        # Number of entries
        f.write(struct.pack('<I', len(keys)))
        # Offset of key index
        f.write(struct.pack('<I', 7 * 4))
        # Offset of value index
        f.write(struct.pack('<I', 7 * 4 + len(keys) * 8))
        # Size of hash table (0 = no hash table)
        f.write(struct.pack('<I', 0))
        # Offset of hash table
        f.write(struct.pack('<I', 0))
        
        # Write key index (length, offset)
        for o1, l1, o2, l2 in offsets:
            f.write(struct.pack('<II', l1, keystart + o1))
        
        # Write value index (length, offset)
        for o1, l1, o2, l2 in offsets:
            f.write(struct.pack('<II', l2, valuestart + o2))
        
        # Write keys
        f.write(ids)
        # Write values
        f.write(strs)
    
    print(f"✓ Compiled: {po_path} -> {mo_path}")
    print(f"  {len(keys)} translations")

def main():
    """Encuentra y compila todos los archivos .po"""
    locale_dir = Path(__file__).parent / 'locale'
    
    if not locale_dir.exists():
        print(f"❌ Locale directory not found: {locale_dir}")
        return
    
    po_files = list(locale_dir.glob('*/LC_MESSAGES/django.po'))
    
    if not po_files:
        print(f"❌ No .po files found in {locale_dir}")
        return
    
    print(f"Found {len(po_files)} .po file(s)")
    print()
    
    for po_file in po_files:
        mo_file = po_file.with_suffix('.mo')
        try:
            compile_po_file(po_file, mo_file)
        except Exception as e:
            print(f"❌ Error compiling {po_file}: {e}")
    
    print()
    print("✅ Compilation complete!")

if __name__ == '__main__':
    main()
