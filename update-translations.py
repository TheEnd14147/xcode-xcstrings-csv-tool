#!/usr/bin/env python3
"""
Automated translation updater for Xcode String Catalogs (.xcstrings)

Updates translations from CSV files (English,Translation format) into your xcstrings file.
Handles edge cases like smart quotes, special characters, and provides detailed reporting.

Usage:
    python update-translations.py --language de --csv path/to/German.csv
    python update-translations.py -l es-419 -c Spanish.csv --dry-run
    python update-translations.py -l fr-CA -c French.csv --verbose
"""

import json
import csv
import argparse
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TranslationUpdate:
    """Represents a single translation update"""
    row: int
    key: str
    english: str
    current: str
    new: str
    status: str  # MATCH, CHANGE, NOT_FOUND, MISMATCH


class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'


def normalize_quotes(text: str) -> str:
    """Normalize smart quotes to straight quotes for comparison"""
    # Replace various quote types with standard ones
    replacements = {
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201C': '"',  # Left double quotation mark
        '\u201D': '"',  # Right double quotation mark
        '\u2032': "'",  # Prime
        '\u2033': '"',  # Double prime
    }
    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result


def fuzzy_match(text1: str, text2: str) -> bool:
    """Check if two strings match after normalizing quotes"""
    return normalize_quotes(text1) == normalize_quotes(text2)


def find_key_for_english(xcstrings_data: dict, target_english: str, verbose: bool = False) -> Optional[str]:
    """Find the xcstrings key for a given English string"""
    target_normalized = normalize_quotes(target_english)

    for key, value in xcstrings_data.get('strings', {}).items():
        if not isinstance(value, dict) or 'localizations' not in value:
            continue

        en_data = value['localizations'].get('en', {})
        if 'stringUnit' in en_data:
            en_value = en_data['stringUnit'].get('value', '')
            if fuzzy_match(en_value, target_english):
                if verbose and en_value != target_english:
                    print(f"  {Colors.CYAN}Fuzzy matched (smart quotes): {key}{Colors.RESET}")
                return key

    return None


def get_current_translation(xcstrings_data: dict, key: str, lang_code: str) -> Optional[str]:
    """Get current translation for a key and language"""
    try:
        return xcstrings_data['strings'][key]['localizations'][lang_code]['stringUnit']['value']
    except (KeyError, TypeError):
        return None


def analyze_updates(csv_path: Path, xcstrings_path: Path, lang_code: str, verbose: bool = False) -> List[TranslationUpdate]:
    """Analyze what updates are needed from the CSV file"""

    print(f"\n{Colors.BOLD}Analyzing translations...{Colors.RESET}")
    print(f"CSV: {csv_path}")
    print(f"xcstrings: {xcstrings_path}")
    print(f"Language: {lang_code}\n")

    # Load xcstrings
    with open(xcstrings_path, 'r', encoding='utf-8') as f:
        xcstrings_data = json.load(f)

    # Load CSV
    updates = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        for row_num, row in enumerate(reader, start=2):
            if len(row) < 2:
                continue

            english, translation = row[0], row[1]

            if verbose:
                print(f"Row {row_num}: {english[:50]}...")

            # Find the key
            key = find_key_for_english(xcstrings_data, english, verbose)

            if key is None:
                updates.append(TranslationUpdate(
                    row=row_num,
                    key="NOT_FOUND",
                    english=english,
                    current="",
                    new=translation,
                    status="NOT_FOUND"
                ))
                if verbose:
                    print(f"  {Colors.RED}✗ Not found in xcstrings{Colors.RESET}")
                continue

            # Get current translation
            current = get_current_translation(xcstrings_data, key, lang_code)

            if current is None:
                status = "NEW"
            elif current == translation:
                status = "MATCH"
            else:
                status = "CHANGE"

            updates.append(TranslationUpdate(
                row=row_num,
                key=key,
                english=english,
                current=current or "",
                new=translation,
                status=status
            ))

            if verbose:
                if status == "CHANGE":
                    print(f"  {Colors.YELLOW}↻ Will update{Colors.RESET}")
                elif status == "MATCH":
                    print(f"  {Colors.GREEN}✓ Already matches{Colors.RESET}")
                elif status == "NEW":
                    print(f"  {Colors.BLUE}+ New translation{Colors.RESET}")

    return updates


def apply_updates(updates: List[TranslationUpdate], xcstrings_path: Path, lang_code: str) -> None:
    """Apply the updates to the xcstrings file"""

    # Load xcstrings
    with open(xcstrings_path, 'r', encoding='utf-8') as f:
        xcstrings_data = json.load(f)

    changes_made = 0

    for update in updates:
        if update.status in ["CHANGE", "NEW"] and update.key != "NOT_FOUND":
            try:
                # Navigate to the translation location
                strings = xcstrings_data['strings']

                # Ensure the key exists
                if update.key not in strings:
                    print(f"{Colors.RED}Warning: Key {update.key} not found, skipping{Colors.RESET}")
                    continue

                # Ensure localizations exists
                if 'localizations' not in strings[update.key]:
                    strings[update.key]['localizations'] = {}

                # Ensure language code exists
                if lang_code not in strings[update.key]['localizations']:
                    strings[update.key]['localizations'][lang_code] = {
                        'stringUnit': {
                            'state': 'translated',
                            'value': ''
                        }
                    }

                # Update the value
                strings[update.key]['localizations'][lang_code]['stringUnit']['value'] = update.new
                strings[update.key]['localizations'][lang_code]['stringUnit']['state'] = 'translated'

                changes_made += 1

            except Exception as e:
                print(f"{Colors.RED}Error updating {update.key}: {e}{Colors.RESET}")

    # Write back to file
    with open(xcstrings_path, 'w', encoding='utf-8') as f:
        json.dump(xcstrings_data, f, ensure_ascii=False, indent=2)

    print(f"\n{Colors.GREEN}✓ Applied {changes_made} updates to {xcstrings_path}{Colors.RESET}")


def print_summary(updates: List[TranslationUpdate]) -> None:
    """Print a summary of the updates"""

    total = len(updates)
    matches = sum(1 for u in updates if u.status == "MATCH")
    changes = sum(1 for u in updates if u.status == "CHANGE")
    new = sum(1 for u in updates if u.status == "NEW")
    not_found = sum(1 for u in updates if u.status == "NOT_FOUND")

    print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}SUMMARY{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    print(f"Total entries in CSV: {total}")
    print(f"{Colors.GREEN}✓ Already matching: {matches} ({matches/total*100:.1f}%){Colors.RESET}")
    print(f"{Colors.YELLOW}↻ Updates needed: {changes} ({changes/total*100:.1f}%){Colors.RESET}")
    print(f"{Colors.BLUE}+ New translations: {new} ({new/total*100:.1f}%){Colors.RESET}")
    print(f"{Colors.RED}✗ Not found: {not_found} ({not_found/total*100:.1f}%){Colors.RESET}")

    # Show changes
    if changes > 0:
        print(f"\n{Colors.BOLD}Changes to be applied:{Colors.RESET}\n")
        for update in updates:
            if update.status == "CHANGE":
                print(f"{Colors.CYAN}{update.key}{Colors.RESET}")
                print(f"  Current: {update.current}")
                print(f"  New:     {update.new}")
                print()

    # Show new translations
    if new > 0:
        print(f"\n{Colors.BOLD}New translations to be added:{Colors.RESET}\n")
        for update in updates:
            if update.status == "NEW":
                print(f"{Colors.CYAN}{update.key}{Colors.RESET}")
                print(f"  New: {update.new}")
                print()

    # Show not found
    if not_found > 0:
        print(f"\n{Colors.BOLD}{Colors.RED}Entries not found in xcstrings:{Colors.RESET}\n")
        for update in updates:
            if update.status == "NOT_FOUND":
                print(f"Row {update.row}: {update.english[:80]}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Update Xcode String Catalog translations from CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update German translations
  python update-translations.py -l de -c German.csv

  # Preview changes without applying (dry run)
  python update-translations.py -l es-419 -c Spanish.csv --dry-run

  # Verbose output showing each row
  python update-translations.py -l fr-CA -c French.csv -v

  # Specify custom xcstrings path
  python update-translations.py -l de -c German.csv -x path/to/Custom.xcstrings
        """
    )

    parser.add_argument('-l', '--language', required=True,
                        help='Language code (e.g., de, es-419, fr-CA)')
    parser.add_argument('-c', '--csv', required=True, type=Path,
                        help='Path to CSV file with English,Translation columns')
    parser.add_argument('-x', '--xcstrings', type=Path,
                        help='Path to xcstrings file (default: auto-detect)')
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='Preview changes without applying them')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    # Validate CSV exists
    if not args.csv.exists():
        print(f"{Colors.RED}Error: CSV file not found: {args.csv}{Colors.RESET}")
        sys.exit(1)

    # Auto-detect xcstrings file
    if args.xcstrings is None:
        # Look for Localizable.xcstrings in common locations
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
            print(f"{Colors.RED}Error: Could not find Localizable.xcstrings{Colors.RESET}")
            print("Please specify the path with --xcstrings")
            sys.exit(1)

    # Validate xcstrings exists
    if not args.xcstrings.exists():
        print(f"{Colors.RED}Error: xcstrings file not found: {args.xcstrings}{Colors.RESET}")
        sys.exit(1)

    # Analyze updates
    updates = analyze_updates(args.csv, args.xcstrings, args.language, args.verbose)

    # Print summary
    print_summary(updates)

    # Apply updates (unless dry run)
    if args.dry_run:
        print(f"\n{Colors.YELLOW}DRY RUN - No changes applied{Colors.RESET}")
        print("Run without --dry-run to apply these changes")
    else:
        changes_needed = sum(1 for u in updates if u.status in ["CHANGE", "NEW"])
        if changes_needed > 0:
            print(f"\n{Colors.BOLD}Applying {changes_needed} updates...{Colors.RESET}")
            apply_updates(updates, args.xcstrings, args.language)
            print(f"\n{Colors.GREEN}✓ Done! Your translations have been updated.{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}✓ No updates needed - all translations already match!{Colors.RESET}")


if __name__ == '__main__':
    main()
