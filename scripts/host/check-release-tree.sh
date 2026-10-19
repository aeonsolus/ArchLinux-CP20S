#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail

repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)
cd "$repo"

failures=0
check_file() {
  if [[ -f $1 ]]; then printf 'OK   %s\n' "$1"; else printf 'MISS %s\n' "$1"; failures=$((failures + 1)); fi
}

for path in README.md LICENSE LICENSE-DOCS docs/CLEAN-INSTALL.md docs/INSTALL.md \
  docs/HARDWARE-SUPPORT.md docs/DESKTOP.md docs/LICENSING.md \
  profiles/core/packages.txt profiles/gnome/packages.txt \
  scripts/host/extract-archarm-rootfs.sh scripts/host/apply-overlay.sh; do
  check_file "$path"
done

while IFS= read -r -d '' script; do
  if bash -n "$script"; then printf 'OK   bash syntax: %s\n' "$script"; else failures=$((failures + 1)); fi
done < <(find scripts -type f -name '*.sh' -print0)

if rg -n --hidden --glob '!.git/**' \
  '(gho_[A-Za-z0-9]{20,}|tskey-[A-Za-z0-9_-]{15,}|-----BEGIN (RSA |OPENSSH )?PRIVATE KEY-----|AKIA[0-9A-Z]{16})' .; then
  echo 'Potential credential material found; review before publication.' >&2
  failures=$((failures + 1))
fi

if rg -n --glob '*.md' '(/home/(aeon|chaos)/|/tmp/|/var/lib/cp20s/arch-root|[0-9a-f]{64})' docs profiles README.md; then
  echo 'Review local paths, device-specific identifiers, or hashes before publication.' >&2
  failures=$((failures + 1))
fi

if (( failures > 0 )); then
  printf 'Release-tree check found %d issue(s).\n' "$failures" >&2
  exit 1
fi
echo 'Release-tree structural checks passed. This does not prove a build or device acceptance.'
