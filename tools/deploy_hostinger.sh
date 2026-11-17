#!/usr/bin/env bash
# Uploads docs/ to Hostinger public_html over TUS. Get URL/AUTH/REST from the Hostinger API
# (hosting_files_generate-upload-url for newquayseamstress.com) and export them first:
#   export HUP_URL=... HUP_AUTH=... HUP_REST=...   then   tools/deploy_hostinger.sh
set -euo pipefail
cd "$(dirname "$0")/../docs"
up(){ f="$1"; d="${f#./}"; s=$(wc -c < "$f" | tr -d ' ')
  a=$(curl -sS -o /dev/null -w "%{http_code}" -X POST "$HUP_URL/$d?override=true" -H "X-Auth: $HUP_AUTH" -H "X-Auth-Rest: $HUP_REST" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $s" -H "Upload-Offset: 0")
  b=204; [ "$s" -gt 0 ] && b=$(curl -sS -o /dev/null -w "%{http_code}" -X PATCH "$HUP_URL/$d?override=true" -H "X-Auth: $HUP_AUTH" -H "X-Auth-Rest: $HUP_REST" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f")
  if [ "$a" = 201 ] && [ "$b" = 204 ]; then echo OK; else echo "FAIL $d $a $b"; fi; }
export -f up
find . -type f ! -name .nojekyll -print0 | xargs -0 -n1 -P6 bash -c 'up "$0"' | sort | uniq -c
