#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: apply-overlay.sh ROOTFS_DIRECTORY" >&2
  exit 2
fi
[[ -d $1 && ! -L $1 ]] || { echo "ROOTFS_DIRECTORY must be an existing directory, not a symlink." >&2; exit 1; }
root=$(realpath -e -- "$1")
[[ $root != / ]] || { echo "Refusing to overlay the host root filesystem." >&2; exit 1; }
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)

while IFS= read -r -d '' source; do
  relative=${source#"$repo/rootfs/"}
  destination="$root/$relative"
  if [[ -e $destination || -L $destination ]]; then
    if [[ ! -f $destination || ! -f $source ]] || ! cmp -s -- "$source" "$destination"; then
      echo "Refusing to overwrite a different target path: $destination" >&2
      exit 1
    fi
  fi
done < <(find "$repo/rootfs" -type f -print0)

echo "Applying the small CP20S overlay to $root"
cp -a -- "$repo/rootfs/." "$root/"
echo "Overlay copied. No service was enabled and no device was modified."
