#!/usr/bin/env python3
"""
Script mejorado para compilar traducciones con compatibilidad Python 3.13
Genera archivos .mo con header UTF-8 explícito en formato gettext estándar
"""
import os
import struct
from pathlib import Path


def parse_po_file(po_path):
    """
    Parse archivo .po y retorna dict de traducciones
    Maneja correctamente multilinea y header
    """
    translations = {}
    current_msgid = []
    current_msgstr = []
    in_msgid = False
    in_msgstr = False
    
    with open(po_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            
            # Skip comments and empty lines outside entries
            if line.startswith('#') or (not line.strip() and not in_msgid and not in_msgstr):
                continue
            
            if line.startswith('msgid '):
                # Save previous entry if exists
                if in_msgstr:
                    msgid_text = ''.join(current_msgid)
                    msgstr_text = ''.join(current_msgstr)
                    translations[msgid_text] = msgstr_text
                
                # Start new msgid
                current_msgid = [line[7:-1] if line.endswith('"') and line.startswith('msgid "') else '']
                current_msgstr = []
                in_msgid = True
                in_msgstr = False
                
            elif line.startswith('msgstr '):
                # Start msgstr
                current_msgstr = [line[8:-1] if line.endswith('"') and line.startswith('msgstr "') else '']
                in_msgid = False
                in_msgstr = True
                
            elif line.startswith('"') and line.endswith('"'):
                # Continuation line
                content = line[1:-1]
                if in_msgid:
                    current_msgid.append(content)
                elif in_msgstr:
                    current_msgstr.append(content)
        
        # Save last entry
        if in_msgstr:
            msgid_text = ''.join(current_msgid)
            msgstr_text = ''.join(current_msgstr)
            translations[msgid_text] = msgstr_text
    
    return translations


def create_mo_file(translations, mo_path):
    """
    Crea archivo .mo en formato gettext estándar
    Compatible con Python 3.13
    """
    # Ensure header exists and declares UTF-8
    # CRITICAL: Replace \\n string escapes with actual newlines for gettext
    if '' not in translations:
        translations[''] = 'Content-Type: text/plain; charset=UTF-8\n'
    else:
        # Force UTF-8 in existing header and convert \\n to real newlines
        header = translations[''].replace('\\n', '\n')  # Convert escape sequences
        if 'charset=' not in header.lower():
            translations[''] = header + 'Content-Type: text/plain; charset=UTF-8\n'
        elif 'utf-8' not in header.lower():
            # Replace any other charset with UTF-8
            import re
            translations[''] = re.sub(
                r'charset=[^\s\n]+',
                'charset=UTF-8',
                header,
                flags=re.IGNORECASE
            )
        else:
            # Header already has UTF-8, just use it with real newlines
            translations[''] = header
    
    # Sort keys (empty string first for header)
    keys = sorted(translations.keys())
    
    # Build key and value tables
    keys_data = b''
    values_data = b''
    offsets = []
    
    for key in keys:
        key_bytes = key.encode('utf-8')
        value_bytes = translations[key].encode('utf-8')
        
        offsets.append({
            'key_len': len(key_bytes),
            'key_offset': len(keys_data),
            'value_len': len(value_bytes),
            'value_offset': len(values_data)
        })
        
        keys_data += key_bytes + b'\x00'
        values_data += value_bytes + b'\x00'
    
    # Calculate table positions
    n = len(keys)
    keys_index_offset = 28  # 7 * 4 bytes for header
    values_index_offset = keys_index_offset + (n * 8)  # each entry is 2 * 4 bytes
    keys_data_offset = values_index_offset + (n * 8)
    values_data_offset = keys_data_offset + len(keys_data)
    
    # Write .mo file
    with open(mo_path, 'wb') as f:
        # Header
        f.write(struct.pack('<I', 0x950412de))  # Magic number (little-endian)
        f.write(struct.pack('<I', 0))            # Version
        f.write(struct.pack('<I', n))            # Number of entries
        f.write(struct.pack('<I', keys_index_offset))    # Offset to keys index
        f.write(struct.pack('<I', values_index_offset))  # Offset to values index
        f.write(struct.pack('<I', 0))            # Hash table size (0 = no hash)
        f.write(struct.pack('<I', 0))            # Hash table offset
        
        # Keys index
        for entry in offsets:
            f.write(struct.pack('<I', entry['key_len']))
            f.write(struct.pack('<I', keys_data_offset + entry['key_offset']))
        
        # Values index
        for entry in offsets:
            f.write(struct.pack('<I', entry['value_len']))
            f.write(struct.pack('<I', values_data_offset + entry['value_offset']))
        
        # Keys data
        f.write(keys_data)
        
        # Values data
        f.write(values_data)
    
    return n


def main():
    """Compila todos los archivos .po encontrados"""
    locale_dir = Path(__file__).parent / 'locale'
    
    if not locale_dir.exists():
        print(f"❌ Locale directory not found: {locale_dir}")
        return
    
    po_files = list(locale_dir.glob('*/LC_MESSAGES/django.po'))
    
    if not po_files:
        print(f"❌ No .po files found in {locale_dir}")
        return
    
    print(f"Found {len(po_files)} .po file(s)")
    print(f"Using Python 3.13 compatible format")
    print()
    
    for po_file in po_files:
        mo_file = po_file.with_suffix('.mo')
        try:
            translations = parse_po_file(po_file)
            count = create_mo_file(translations, mo_file)
            print(f"✓ Compiled: {po_file.parent.parent.name}/{po_file.parent.name}/{po_file.name}")
            print(f"  {count} translations (including header)")
        except Exception as e:
            print(f"❌ Error compiling {po_file}: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print("✅ Compilation complete!")
    print("Note: Files are Python 3.13 compatible with explicit UTF-8 charset")


if __name__ == '__main__':
    main()
