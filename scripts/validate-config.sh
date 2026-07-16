#!/usr/bin/env bash

set -euo pipefail

DIRECTORIES=("legacy" "vanilla" "active")
validated_files=0

for directory in "${DIRECTORIES[@]}"; do
  [[ -d "$directory" ]] || continue

  while IFS= read -r -d '' file; do
    echo "Validating XML: $file"
    xmllint --noout "$file"
    validated_files=$((validated_files + 1))
  done < <(find "$directory" -type f -name '*.xml' -print0)

  while IFS= read -r -d '' file; do
    echo "Validating JSON: $file"
    python3 -m json.tool "$file" > /dev/null
    validated_files=$((validated_files + 1))
  done < <(find "$directory" -type f -name '*.json' -print0)
done

echo "Validation successful: $validated_files configuration files checked."
