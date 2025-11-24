# Translation Instructions

Thank you for translating Puppy Potty Trainer!

## CSV Format

You will receive a CSV file with two columns:

| English | Translation |
|---------|-------------|
| Hello World | *(your translation here)* |
| Welcome to %@ | *(your translation here)* |

## Instructions

1. **DO NOT edit the "English" column** - Leave it exactly as is
2. **ONLY edit the "Translation" column** - Put your translations here
3. **Preserve placeholders** - Keep `%@`, `%lld`, `%d` exactly as shown
4. **Preserve formatting** - Keep quotes, line breaks, and punctuation

## Important Rules

### Placeholders MUST Be Preserved

❌ **Wrong:**
```csv
English,Translation
"Welcome to %@","Willkommen"
```

✅ **Correct:**
```csv
English,Translation
"Welcome to %@","Willkommen bei %@"
```

### Placeholder Types

- `%@` = Text (e.g., app name, time)
- `%lld` = Number (e.g., count, days)
- `%d` = Integer number

These **must appear in your translation** exactly as shown!

### Special Characters

If the English has special characters, preserve them:
- Quotes: `"Text"`
- Colons: `Time:`
- Newlines: Keep line breaks
- Commas: Keep punctuation

### Header Row

The first row (`English,Translation`) is a header - **do not translate it**.

## Example

**Given CSV:**
```csv
English,Translation
Emerging,
"Patterns start forming around 15 events!",
"%lld / 15 events logged",
```

**Your completed CSV:**
```csv
English,Translation
Emerging,Aufkommend
"Patterns start forming around 15 events!","Erste Muster entstehen nach etwa 15 Missgeschicken!"
"%lld / 15 events logged","%lld / 15 Missgeschicke erfasst"
```

## Tools You Can Use

- Microsoft Excel
- Apple Numbers
- Google Sheets
- Any text editor

**Save as:** CSV (Comma Separated Values, UTF-8 encoding)

## Questions?

If any English text is unclear or needs context, please ask! We're happy to provide:
- Screenshots showing where text appears
- Context about what the text means
- Character/length limits if applicable

## Return Format

Please return the CSV file with:
- Same filename (or add your language code)
- UTF-8 encoding
- All translations filled in

Thank you! 🙏
