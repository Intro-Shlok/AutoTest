#!/usr/bin/env bash
# Unified enrichment pipeline — runs all extractors in dependency order.
# Usage: bash src/scripts/enrichment/run-enrichment.sh

set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "========================================="
echo "  AutoTest Database Enrichment Pipeline"
echo "========================================="

echo ""
echo "=== Step 1: RedTeaming (Aho-Corasick + state-machine lexer) ==="
python3 src/scripts/enrichment/extract-redteaming.py

echo ""
echo "=== Step 2: LOLBAS (detections + mitre_ids + examples) ==="
python3 src/scripts/enrichment/extract-lolbas.py

echo ""
echo "=== Step 3: GTFOArgs (argument injection examples) ==="
python3 src/scripts/enrichment/extract-gtfoargs.py

echo ""
echo "=== Step 4: WADComs (items + services + attack_types) ==="
python3 src/scripts/enrichment/extract-wadcoms.py

echo ""
echo "=== Step 5: Darkiros (parameterized examples) ==="
python3 src/scripts/enrichment/extract-darkiros.py

echo ""
echo "=== Step 6: NetRunners (template examples) ==="
python3 src/scripts/enrichment/extract-netrunners.py

echo ""
echo "=== Step 7: cheat.sheets (command examples) ==="
python3 src/scripts/enrichment/extract-cheatsheets.py

echo ""
echo "=== Step 8: cheat.sheets (related_tools from see_also) ==="
python3 src/scripts/enrichment/extract-seealso.py

echo ""
echo "=== Step 9: Reverse Shell payloads (revshells) ==="
python3 src/scripts/enrichment/extract-revshells.py

echo ""
echo "=== Step 10: Validate frontmatter ==="
node src/scripts/validate-frontmatter.js

echo ""
echo "=== Step 11: Build site + API ==="
npm run build
node src/scripts/build-api.js

echo ""
echo "========================================="
echo "  Enrichment pipeline complete"
echo "========================================="
