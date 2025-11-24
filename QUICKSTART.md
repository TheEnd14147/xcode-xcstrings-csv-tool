# Translation Update - Quick Reference

## Single Command to Update Translations

```bash
python3 Scripts/update-translations.py -l LANGUAGE_CODE -c path/to/file.csv
```

## Common Commands

| Task | Command |
|------|---------|
| Update German | `python3 Scripts/update-translations.py -l de -c German.csv` |
| Update Spanish | `python3 Scripts/update-translations.py -l es-419 -c Spanish.csv` |
| Preview first | `python3 Scripts/update-translations.py -l de -c German.csv --dry-run` |
| See details | `python3 Scripts/update-translations.py -l de -c German.csv -v` |

## Language Codes Quick Reference

```
de          German
es-419      Spanish (Latin America)
fr-CA       French (Canada)
pt-BR       Portuguese (Brazil)
zh-Hans     Chinese (Simplified)
zh-Hant     Chinese (Traditional)
ko          Korean
ja          Japanese
it          Italian
nl          Dutch
ru          Russian
th          Thai
vi          Vietnamese
id          Indonesian
fil         Filipino
```

## CSV Format

```csv
English,Translation
"First string","Translated string"
"Text with %@ placeholder","Text mit %@ Platzhalter"
```

**Must have:**
- Header row (English,Translation)
- Exact English match from xcstrings
- Preserved placeholders (%lld, %@, etc.)

## Workflow

1. Get CSV from translator
2. `--dry-run` to preview
3. Run without `--dry-run` to apply
4. Build app to test
5. Commit changes

## Example

```bash
# 1. Preview
python3 Scripts/update-translations.py -l de -c German.csv --dry-run

# 2. Apply
python3 Scripts/update-translations.py -l de -c German.csv

# 3. Verify
git diff "Puppy Potty Trainer/Resources/Localizable.xcstrings"

# 4. Commit
git add "Puppy Potty Trainer/Resources/Localizable.xcstrings"
git commit -m "Update German translations"
```

**Time saved: 30 minutes → 30 seconds!**
