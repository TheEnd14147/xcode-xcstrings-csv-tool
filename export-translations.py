#!/usr/bin/env python3
"""
Export translations from Xcode String Catalogs (.xcstrings) to CSV format

Extracts translations for a specific language and creates a CSV file
that can be sent to translators or used for review.

Usage:
    python export-translations.py --language de --output German.csv
    python export-translations.py -l es-419 -o Spanish.csv
"""

import json
import csv
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'


def export_translations(xcstrings_path: Path, lang_code: str, include_english: bool = True) -> List[Tuple[str, str, str]]:
    """
    Export translations from xcstrings file

    Returns list of tuples: (key, english, translation)
    """

    with open(xcstrings_path, 'r', encoding='utf-8') as f:
        xcstrings_data = json.load(f)

    translations = []

    for key, value in xcstrings_data.get('strings', {}).items():
        if not isinstance(value, dict) or 'localizations' not in value:
            continue

        # Get English text
        en_data = value['localizations'].get('en', {})
        if 'stringUnit' not in en_data:
            continue
        english = en_data['stringUnit'].get('value', '')

        # Get target language translation
        lang_data = value['localizations'].get(lang_code, {})
        if 'stringUnit' in lang_data:
            translation = lang_data['stringUnit'].get('value', '')
        else:
            translation = ""

        translations.append((key, english, translation))

    # Sort by key for consistent output
    translations.sort(key=lambda x: x[0])

    return translations


def write_csv(translations: List[Tuple[str, str, str]], output_path: Path, include_keys: bool = False):
    """Write translations to CSV file"""

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        if include_keys:
            writer = csv.writer(f)
            writer.writerow(['Key', 'English', 'Translation'])
            for key, english, translation in translations:
                writer.writerow([key, english, translation])
        else:
            writer = csv.writer(f)
            writer.writerow(['English', 'Translation'])
            for key, english, translation in translations:
                writer.writerow([english, translation])


def main():
    parser = argparse.ArgumentParser(
        description='Export translations from Xcode String Catalog to CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export German translations
  python export-translations.py -l de -o German.csv

  # Export with key column included
  python export-translations.py -l es-419 -o Spanish.csv --include-keys

  # Export from custom xcstrings file
  python export-translations.py -l de -o German.csv -x path/to/Custom.xcstrings
        """
    )

    parser.add_argument('-l', '--language', required=True,
                        help='Language code (e.g., de, es-419, fr-CA)')
    parser.add_argument('-o', '--output', required=True, type=Path,
                        help='Output CSV file path')
    parser.add_argument('-x', '--xcstrings', type=Path,
                        help='Path to xcstrings file (default: auto-detect)')
    parser.add_argument('-k', '--include-keys', action='store_true',
                        help='Include key column in CSV (useful for reference)')

    args = parser.parse_args()

    # Auto-detect xcstrings file
    if args.xcstrings is None:
        search_paths = [
            Path.cwd() / "Puppy Potty Trainer" / "Resources" / "Localizable.xcstrings",
            Path.cwd() / "Resources" / "Localizable.xcstrings",
            Path.cwd() / "Localizable.xcstrings",
        ]

        for path in search_paths:
            if path.exists():
                args.xcstrings = path
                break

        if args.xcstrings is None:
            print(f"{Colors.YELLOW}Error: Could not find Localizable.xcstrings{Colors.RESET}")
            print("Please specify the path with --xcstrings")
            sys.exit(1)

    # Validate xcstrings exists
    if not args.xcstrings.exists():
        print(f"{Colors.YELLOW}Error: xcstrings file not found: {args.xcstrings}{Colors.RESET}")
        sys.exit(1)

    print(f"\n{Colors.BOLD}Exporting translations...{Colors.RESET}")
    print(f"Source: {args.xcstrings}")
    print(f"Language: {args.language}")
    print(f"Output: {args.output}\n")

    # Export translations
    translations = export_translations(args.xcstrings, args.language)

    # Count statistics
    total = len(translations)
    translated = sum(1 for _, _, trans in translations if trans)
    missing = total - translated

    print(f"{Colors.BOLD}Statistics:{Colors.RESET}")
    print(f"Total strings: {total}")
    print(f"{Colors.GREEN}Translated: {translated} ({translated/total*100:.1f}%){Colors.RESET}")
    if missing > 0:
        print(f"{Colors.YELLOW}Missing: {missing} ({missing/total*100:.1f}%){Colors.RESET}")

    # Write CSV
    write_csv(translations, args.output, args.include_keys)

    print(f"\n{Colors.GREEN}✓ Exported to {args.output}{Colors.RESET}")

    if missing > 0:
        print(f"\n{Colors.YELLOW}Note: {missing} strings have no translation yet (empty cells in CSV){Colors.RESET}")


if __name__ == '__main__':
    main()
