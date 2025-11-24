#!/bin/bash
# Batch update all language translations from CSV files

set -e  # Exit on error

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# Function to get language code from filename
get_lang_code() {
    case "$1" in
        "Dutch.csv") echo "nl" ;;
        "Filipino.csv") echo "fil" ;;
        "French.csv") echo "fr-CA" ;;
        "Indonesian.csv") echo "id" ;;
        "Japanese.csv") echo "ja" ;;
        "Portuguese.csv") echo "pt-BR" ;;
        "Russian.csv") echo "ru" ;;
        "Thai.csv") echo "th" ;;
        *) echo "" ;;
    esac
}

# CSV directory (can be overridden)
CSV_DIR="${1:-Languages}"

# Check if directory exists
if [ ! -d "$CSV_DIR" ]; then
    echo -e "${YELLOW}Error: Directory '$CSV_DIR' not found${RESET}"
    exit 1
fi

# Check if dry run
DRY_RUN=""
if [ "$2" = "--dry-run" ]; then
    DRY_RUN="--dry-run"
    echo -e "${YELLOW}${BOLD}DRY RUN MODE - No changes will be applied${RESET}\n"
fi

echo -e "${BOLD}Updating translations from $CSV_DIR/${RESET}\n"

# Process each CSV file
SUCCESS=0
FAILED=0

for csv_file in "$CSV_DIR"/*.csv; do
    # Get filename without path
    filename=$(basename "$csv_file")

    # Get language code
    lang_code=$(get_lang_code "$filename")

    # Skip if not in our mapping
    if [ -z "$lang_code" ]; then
        echo -e "${YELLOW}⊘ Skipping $filename (no language code mapping)${RESET}"
        continue
    fi

    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}Processing: $filename → $lang_code${RESET}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}\n"

    # Run the update script
    if python3 Scripts/update-translations.py -l "$lang_code" -c "$csv_file" $DRY_RUN; then
        SUCCESS=$((SUCCESS + 1))
        echo -e "\n${GREEN}✓ $filename completed${RESET}\n"
    else
        FAILED=$((FAILED + 1))
        echo -e "\n${YELLOW}✗ $filename failed${RESET}\n"
    fi
done

# Summary
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${BOLD}BATCH UPDATE COMPLETE${RESET}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}\n"

echo -e "${GREEN}✓ Successful: $SUCCESS${RESET}"
if [ $FAILED -gt 0 ]; then
    echo -e "${YELLOW}✗ Failed: $FAILED${RESET}"
fi

echo ""

if [ -n "$DRY_RUN" ]; then
    echo -e "${YELLOW}This was a dry run. Run without --dry-run to apply changes.${RESET}"
else
    echo -e "${GREEN}All translations have been updated!${RESET}"
    echo -e "Review changes: ${CYAN}git diff \"Puppy Potty Trainer/Resources/Localizable.xcstrings\"${RESET}"
fi
