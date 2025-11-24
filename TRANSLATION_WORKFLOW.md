# Complete Translation Workflow

This guide covers the complete workflow for managing translations in Puppy Potty Trainer.

## Overview

You now have two powerful scripts:
1. **export-translations.py** - Extract translations to CSV for translators
2. **update-translations.py** - Import updated translations back into the app

## Complete Workflow

### Step 1: Export Current Translations

When you need to send translations to a translator:

```bash
python3 Scripts/export-translations.py -l de -o German-for-review.csv
```

This creates a CSV with:
- Column 1: English text
- Column 2: Current German translation

Send this CSV to your translator.

### Step 2: Receive Updated Translations

Your translator sends back the CSV with updated translations in the second column.

### Step 3: Preview Changes

Before applying updates, do a dry run:

```bash
python3 Scripts/update-translations.py -l de -c German-updated.csv --dry-run
```

This shows:
- How many translations will change
- Exactly what the changes are
- Any missing or problematic entries

### Step 4: Apply Updates

If everything looks good:

```bash
python3 Scripts/update-translations.py -l de -c German-updated.csv
```

Takes ~1 second to update all translations!

### Step 5: Test in App

Build and run your app to verify the translations look good in context.

### Step 6: Commit

```bash
git add "Puppy Potty Trainer/Resources/Localizable.xcstrings"
git commit -m "Update German translations"
```

## Updating Multiple Languages

You can update all your languages quickly:

```bash
# Export all languages
python3 Scripts/export-translations.py -l de -o German.csv
python3 Scripts/export-translations.py -l es-419 -o Spanish.csv
python3 Scripts/export-translations.py -l fr-CA -o French.csv
python3 Scripts/export-translations.py -l pt-BR -o Portuguese.csv
python3 Scripts/export-translations.py -l zh-Hans -o Chinese-Simplified.csv
python3 Scripts/export-translations.py -l zh-Hant -o Chinese-Traditional.csv
python3 Scripts/export-translations.py -l ko -o Korean.csv
python3 Scripts/export-translations.py -l ja -o Japanese.csv
python3 Scripts/export-translations.py -l it -o Italian.csv
python3 Scripts/export-translations.py -l nl -o Dutch.csv
python3 Scripts/export-translations.py -l ru -o Russian.csv
python3 Scripts/export-translations.py -l th -o Thai.csv
python3 Scripts/export-translations.py -l vi -o Vietnamese.csv
python3 Scripts/export-translations.py -l id -o Indonesian.csv
python3 Scripts/export-translations.py -l fil -o Filipino.csv

# After receiving updates, import them all
python3 Scripts/update-translations.py -l de -c German.csv
python3 Scripts/update-translations.py -l es-419 -c Spanish.csv
python3 Scripts/update-translations.py -l fr-CA -c French.csv
# ... etc
```

**Time for all 15 languages: ~30 seconds** (vs several hours manually!)

## When to Use Each Script

| Task | Script | Command |
|------|--------|---------|
| Send to translator | export | `export-translations.py -l de -o file.csv` |
| Get current translations | export | `export-translations.py -l de -o file.csv` |
| Review translations | export | `export-translations.py -l de -o file.csv --include-keys` |
| Update from translator | update | `update-translations.py -l de -c file.csv` |
| Verify before applying | update | `update-translations.py -l de -c file.csv --dry-run` |

## Tips for Working with Translators

### Provide Context

When exporting, consider using `--include-keys`:

```bash
python3 Scripts/export-translations.py -l de -o German.csv --include-keys
```

This adds a "Key" column showing where each string appears (e.g., `onboarding.welcome.headline`).

### CSV Format for Translators

Make sure your translator knows:
- **First column = English (DO NOT EDIT)**
- **Second column = Translation (EDIT THIS)**
- **Preserve placeholders** like %lld, %@, etc.
- **Preserve formatting** like line breaks, quotes

Example you can send:

> Please update only the "Translation" column. Do not modify the "English" column.
> Keep placeholders like %@ and %lld exactly as shown.

### Version Control

Keep dated versions:
```
Translations/
├── German-2024-11-24.csv
├── German-2024-12-01.csv
└── Spanish-2024-11-24.csv
```

## Troubleshooting

### "Not found in xcstrings"

The English text changed in your app but the CSV still has the old text.

**Solution:**
1. Export fresh translations: `export-translations.py -l de -o German-fresh.csv`
2. Copy the updated translation for that string to the new CSV
3. Import the new CSV

### Missing Translations

Export shows some translations are missing:

```
Translated: 45 (86.5%)
Missing: 7 (13.5%)
```

**Solution:**
1. Export with `--include-keys` to see which keys are missing
2. Add translations to the CSV (empty cells will appear for missing ones)
3. Import when complete

### Bulk Replace Needed

You need to change "Unfall" → "Missgeschick" across all languages:

**Solution:**
1. Export each language
2. Use find/replace in Excel/Numbers on each CSV
3. Import all updated CSVs

Much faster than editing xcstrings directly!

## Benefits of This Workflow

| Old Workflow | New Workflow |
|-------------|-------------|
| Edit JSON manually | Work with CSV files |
| 30+ minutes per language | 30 seconds per language |
| Error-prone | Automated validation |
| Hard to track changes | Clear diff in git |
| Translator needs Xcode | Translator uses Excel |
| Hard to review | Easy to review in spreadsheet |

## Advanced: Batch Processing

Create a script to update all languages at once:

```bash
#!/bin/bash
# update-all-languages.sh

for lang_csv in Translations/*.csv; do
    # Extract language code from filename
    lang=$(basename "$lang_csv" .csv)

    echo "Updating $lang..."
    python3 Scripts/update-translations.py -l "$lang" -c "$lang_csv"
done

echo "All languages updated!"
```

Make it executable:
```bash
chmod +x update-all-languages.sh
./update-all-languages.sh
```

---

## Summary

**Exporting:** `export-translations.py` → sends CSV to translator
**Importing:** `update-translations.py` → brings updates back

**Time saved per update cycle: ~4 hours → 5 minutes**

🎉 Enjoy your automated translation workflow!
