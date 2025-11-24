#!/bin/bash
# Setup script for xcstrings translation automation
# Run this to configure the tools for your project

set -e

echo "🚀 Setting up Xcode String Catalog Translation Automation"
echo ""

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    echo "Install via: xcode-select --install"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Make scripts executable
chmod +x update-translations.py
chmod +x export-translations.py
chmod +x update-all-languages.sh

echo "✅ Made scripts executable"

# Test scripts
echo ""
echo "Testing scripts..."

if python3 update-translations.py --help > /dev/null 2>&1; then
    echo "✅ update-translations.py works"
else
    echo "❌ update-translations.py failed"
    exit 1
fi

if python3 export-translations.py --help > /dev/null 2>&1; then
    echo "✅ export-translations.py works"
else
    echo "❌ export-translations.py failed"
    exit 1
fi

# Look for xcstrings file
echo ""
echo "Looking for Localizable.xcstrings..."

FOUND_XCSTRINGS=""
SEARCH_PATHS=(
    "../*/Resources/Localizable.xcstrings"
    "../Resources/Localizable.xcstrings"
    "../Localizable.xcstrings"
    "../../*/Resources/Localizable.xcstrings"
)

for path_pattern in "${SEARCH_PATHS[@]}"; do
    for path in $path_pattern; do
        if [ -f "$path" ]; then
            FOUND_XCSTRINGS="$path"
            echo "✅ Found: $path"
            break 2
        fi
    done
done

if [ -z "$FOUND_XCSTRINGS" ]; then
    echo "⚠️  Could not auto-detect Localizable.xcstrings"
    echo "   You'll need to specify the path with -x flag"
else
    echo ""
    echo "Example usage:"
    echo "  python3 update-translations.py -l de -c German.csv"
fi

# Create example CSV if needed
if [ ! -f "example.csv" ]; then
    cat > example.csv << 'EOF'
English,Translation
"Hello World","Hallo Welt"
"Welcome to %@","Willkommen bei %@"
"%lld items","%lld Artikel"
EOF
    echo ""
    echo "✅ Created example.csv as a template"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Quick start:"
echo "  1. Export translations: python3 export-translations.py -l de -o German.csv"
echo "  2. Update translations: python3 update-translations.py -l de -c German.csv"
echo ""
echo "Read README.md for full documentation"
echo ""
