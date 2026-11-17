#!/usr/bin/env bash
# Full quality gate: readable build -> link/SEO self-check, HTML validation, Schema.org validation -> final minified build.
set -e
cd "$(dirname "$0")/.."
python3 build.py --pretty
python3 selfcheck.py
npx -y html-validate@8 "docs/**/*.html"
python3 tools/validate_schema.py
python3 build.py
echo "All checks passed; docs/ holds the minified production build."
