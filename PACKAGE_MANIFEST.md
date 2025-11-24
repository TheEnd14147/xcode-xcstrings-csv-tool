# Package Manifest

## Files to Share on GitHub

### Core Scripts (Required)
- `update-translations.py` - Import CSV → xcstrings
- `export-translations.py` - Export xcstrings → CSV
- `update-all-languages.sh` - Batch update multiple languages

### Documentation (Required)
- `README-GITHUB.md` - Main README (rename to README.md when publishing)
- `INSTALLATION.md` - Setup instructions
- `LICENSE` - MIT License

### Additional Files (Recommended)
- `setup.sh` - One-command setup script
- `QUICKSTART.md` - Quick reference guide
- `TRANSLATION_WORKFLOW.md` - Complete workflow examples
- `TRANSLATOR_INSTRUCTIONS.md` - Guide for translators
- `TRANSLATOR_TEMPLATE.csv` - Example CSV template

## GitHub Repository Structure

```
xcstrings-csv-tools/
├── README.md                      (README-GITHUB.md renamed)
├── LICENSE
├── INSTALLATION.md
├── update-translations.py
├── export-translations.py
├── update-all-languages.sh
├── setup.sh
├── docs/
│   ├── QUICKSTART.md
│   ├── TRANSLATION_WORKFLOW.md
│   └── TRANSLATOR_INSTRUCTIONS.md
└── examples/
    └── example.csv
```

## How to Publish

### Option 1: Standalone Repository

1. Create new GitHub repo: `xcstrings-csv-tools`
2. Copy files from Scripts/ directory
3. Rename `README-GITHUB.md` to `README.md`
4. Organize docs/ and examples/ subdirectories
5. Add GitHub topics: `ios`, `localization`, `xcode`, `automation`, `i18n`

### Option 2: Keep in Main Project

1. Keep Scripts/ directory as-is
2. Add section to main README linking to Scripts/README-GITHUB.md
3. Others can copy the Scripts/ folder to their projects

### Option 3: Publish as Gist

Create a GitHub Gist with:
- update-translations.py
- export-translations.py
- README-GITHUB.md

## Recommended GitHub Description

> Automate Xcode String Catalog (.xcstrings) translations. Update iOS/macOS localizations from CSV files in seconds. Zero dependencies, pure Python 3.

## Keywords/Topics

- xcode
- ios
- macos
- localization
- internationalization
- i18n
- l10n
- string-catalog
- xcstrings
- translation
- automation
- csv
- python

## Files NOT to Include

These are project-specific:
- `README.md` (your project-specific one)
- Any language-specific CSV files (German.csv, etc.)
- Project configuration specific to Puppy Potty Trainer

## Publishing Checklist

- [ ] Remove project-specific references
- [ ] Test scripts on clean install
- [ ] Add usage examples with generic project names
- [ ] Add screenshot/demo GIF if possible
- [ ] Create releases/tags for versions
- [ ] Set up GitHub Actions for testing (optional)
- [ ] Add contributing guidelines
- [ ] Add issue templates
