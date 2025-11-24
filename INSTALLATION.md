# Installation Guide

## For Your Own Project

### Option 1: Copy Scripts Directly

1. **Create Scripts directory** in your project:
   ```bash
   mkdir Scripts
   cd Scripts
   ```

2. **Copy these files:**
   - `update-translations.py`
   - `export-translations.py`
   - `update-all-languages.sh`
   - `README-GITHUB.md` (rename to README.md)
   - `LICENSE`

3. **Make executable:**
   ```bash
   chmod +x update-all-languages.sh
   chmod +x update-translations.py
   chmod +x export-translations.py
   ```

4. **Test it:**
   ```bash
   python3 update-translations.py --help
   ```

### Option 2: Git Submodule (if we create a repo)

```bash
git submodule add https://github.com/username/xcstrings-tools Scripts/xcstrings-tools
```

## Auto-Detection Setup

The scripts auto-detect your `Localizable.xcstrings` file in these locations:

1. `<ProjectName>/Resources/Localizable.xcstrings`
2. `Resources/Localizable.xcstrings`
3. `Localizable.xcstrings`

**To customize**, edit the search paths in both Python scripts:

```python
search_paths = [
    Path.cwd() / "YourApp" / "Resources" / "Localizable.xcstrings",
    Path.cwd() / "Resources" / "Localizable.xcstrings",
    # Add your custom paths here
]
```

## Batch Script Configuration

Edit `update-all-languages.sh` to match your language files:

```bash
get_lang_code() {
    case "$1" in
        "German.csv") echo "de" ;;
        "Spanish.csv") echo "es-419" ;;
        # Add your CSV filenames and language codes
        *) echo "" ;;
    esac
}
```

## Directory Structure

Recommended setup:

```
YourProject/
├── YourApp/
│   └── Resources/
│       └── Localizable.xcstrings
├── Scripts/
│   ├── update-translations.py
│   ├── export-translations.py
│   ├── update-all-languages.sh
│   ├── README.md
│   └── LICENSE
└── Translations/  (optional - for CSV files)
    ├── German.csv
    ├── Spanish.csv
    └── French.csv
```

## Verify Installation

Run these commands to verify everything works:

```bash
# Test update script
python3 Scripts/update-translations.py --help

# Test export script
python3 Scripts/export-translations.py --help

# Test batch script
./Scripts/update-all-languages.sh --help
```

## Requirements

- **Python 3.6+** (comes with macOS)
- **Xcode 15+** (for String Catalogs)
- **No external packages** - uses Python standard library only

## Troubleshooting

### "command not found: python3"

macOS includes Python 3. If missing, install via:
```bash
xcode-select --install
```

### "Permission denied"

Make scripts executable:
```bash
chmod +x Scripts/*.sh Scripts/*.py
```

### Scripts can't find xcstrings

Specify path explicitly:
```bash
python3 update-translations.py -l de -c German.csv -x "Path/To/Localizable.xcstrings"
```

## Next Steps

1. Export your first translation: `python3 export-translations.py -l de -o German.csv`
2. Read the main README for usage examples
3. Set up your batch script with your languages
4. Integrate into your workflow!
