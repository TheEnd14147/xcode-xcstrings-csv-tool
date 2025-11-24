# Xcode String Catalog Translation Automation

  > Python toolkit to automate iOS/macOS localization with Xcode String Catalogs (.xcstrings)

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
  [![Platform](https://img.shields.io/badge/platform-iOS%20%7C%20macOS-lightgrey.svg)](https://developer.apple.com)

  **Update translations in seconds instead of hours.** Automate your Xcode String Catalog
  (.xcstrings) workflows with simple CSV files.

  ## Problem
  Manually updating translations across multiple languages in Xcode String Catalogs is:
  - ⏱️ Time-consuming (hours per update)
  - 🐛 Error-prone (copy-paste mistakes)
  - 😫 Tedious for translators (need Xcode access)

  ## Solution
  Automate with CSV workflows:
  - ⚡ Update 10+ languages in 30 seconds
  - ✅ Zero copy-paste errors
  - 😊 Translators work with familiar CSV/Excel files
  
  Automate your iOS/macOS localization workflow. Update Xcode `.xcstrings` files from CSV files in seconds instead of hours.

## Features

- ✅ **Automatic key mapping** - Matches English strings to xcstrings keys
- ✅ **Smart quote handling** - Handles Unicode smart quotes vs straight quotes
- ✅ **Special character preservation** - Correctly handles %lld, %@, etc.
- ✅ **Dry run mode** - Preview changes before applying
- ✅ **Batch processing** - Update multiple languages at once
- ✅ **Export to CSV** - Send translations to translators
- ✅ **No dependencies** - Pure Python 3 (standard library only)

## Quick Start

### 1. Update translations from CSV

```bash
python3 update-translations.py -l de -c German.csv
```

### 2. Export translations to CSV

```bash
python3 export-translations.py -l de -o German.csv
```

### 3. Batch update all languages

```bash
./update-all-languages.sh Languages/
```

## Installation

1. **Copy scripts to your project:**
   ```bash
   mkdir Scripts
   cd Scripts
   # Copy update-translations.py, export-translations.py, update-all-languages.sh
   chmod +x update-all-languages.sh
   ```

2. **No other dependencies needed!** Uses Python 3 standard library only.

## CSV Format

Your CSV must have exactly 2 columns:

```csv
English,Translation
"Hello World","Hallo Welt"
"Welcome to %@","Willkommen bei %@"
```

**Important:**
- First row is header (will be skipped)
- Column 1: English text (must match exactly)
- Column 2: Translation
- Preserve placeholders like %@, %lld

## Usage

### Update Single Language

```bash
python3 update-translations.py --language de --csv German.csv
```

**Options:**
- `-l, --language` - Language code (de, es-419, fr-CA, etc.)
- `-c, --csv` - Path to CSV file
- `-x, --xcstrings` - Path to xcstrings file (auto-detected by default)
- `-d, --dry-run` - Preview without applying
- `-v, --verbose` - Show detailed progress

### Export Translations

```bash
python3 export-translations.py --language de --output German.csv
```

**Options:**
- `-l, --language` - Language code
- `-o, --output` - Output CSV path
- `-k, --include-keys` - Include key column (useful for reference)

### Batch Update Multiple Languages

Edit `update-all-languages.sh` to add your language mappings:

```bash
get_lang_code() {
    case "$1" in
        "German.csv") echo "de" ;;
        "Spanish.csv") echo "es-419" ;;
        "French.csv") echo "fr-CA" ;;
        # Add your languages here
        *) echo "" ;;
    esac
}
```

Then run:

```bash
./update-all-languages.sh path/to/csvs/
```

## Common Language Codes

| Language | Code | Language | Code |
|----------|------|----------|------|
| German | `de` | Spanish (Latin America) | `es-419` |
| French (Canada) | `fr-CA` | Portuguese (Brazil) | `pt-BR` |
| Chinese (Simplified) | `zh-Hans` | Chinese (Traditional) | `zh-Hant` |
| Japanese | `ja` | Korean | `ko` |
| Italian | `it` | Dutch | `nl` |
| Russian | `ru` | Thai | `th` |
| Vietnamese | `vi` | Indonesian | `id` |
| Filipino | `fil` | | |

## Workflow Example

### Complete Translation Update Cycle

```bash
# 1. Export current translations for translator
python3 export-translations.py -l de -o German-for-review.csv

# 2. Send to translator, receive German-updated.csv

# 3. Preview changes
python3 update-translations.py -l de -c German-updated.csv --dry-run

# 4. Apply updates
python3 update-translations.py -l de -c German-updated.csv

# 5. Verify and commit
git diff path/to/Localizable.xcstrings
git add path/to/Localizable.xcstrings
git commit -m "Update German translations"
```

### Batch Update All Languages

```bash
# Export all languages
for lang in de es-419 fr-CA ja; do
    python3 export-translations.py -l $lang -o "${lang}.csv"
done

# After receiving updates, batch import
./update-all-languages.sh .
```

## Output Explanation

The scripts provide color-coded feedback:

- **Green ✓** - Already matching (no change needed)
- **Yellow ↻** - Will be updated
- **Blue +** - New translation being added
- **Red ✗** - English text not found in xcstrings

## Troubleshooting

### "Not found in xcstrings"

The English text in your CSV doesn't match the xcstrings file.

**Solution:** Export fresh translations and update from there:
```bash
python3 export-translations.py -l de -o German-fresh.csv
```

### "Could not find Localizable.xcstrings"

**Solution:** Specify the path explicitly:
```bash
python3 update-translations.py -l de -c German.csv -x path/to/Localizable.xcstrings
```

### Smart Quotes Warning

Your xcstrings has Unicode smart quotes (') but CSV has straight quotes ('). This is handled automatically with fuzzy matching.

## Requirements

- Python 3.6 or later
- Xcode String Catalog (.xcstrings) format
- No external dependencies

## Performance

- Handles 50+ strings in < 1 second
- Scales to hundreds of strings
- Batch updates 10+ languages in seconds

## Time Savings

| Task | Manual | Automated |
|------|--------|-----------|
| Single language update | 30 min | 10 sec |
| 10+ languages | 4+ hours | 30 sec |
| Export for translator | Manual | 5 sec |

## License

MIT License - Feel free to use in your projects!

## Contributing

Found a bug or have a feature request? Please open an issue!

## Tips

1. **Always dry-run first** - Use `--dry-run` to preview
2. **Keep CSV files versioned** - Track translation history
3. **Test in simulator** - Verify translations in UI
4. **Use include-keys for context** - Export with `-k` flag for translator reference

## Credits

Built to simplify iOS/macOS localization workflows. Works with Xcode 15+ String Catalogs.

---

**Star this repo if it helps your workflow! 🌟**
## Keywords
  <!-- For search engines -->
  Xcode localization, iOS internationalization, macOS i18n, String Catalog automation,
  xcstrings tool, translation workflow, localization automation, Swift localization,
  CSV translation import, Xcode 15 String Catalogs, iOS l10n, macOS localization tool