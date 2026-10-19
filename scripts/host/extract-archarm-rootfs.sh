#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage: extract-archarm-rootfs.sh ARCHIVE SIGNATURE TRUSTED_KEYRING DESTINATION

Verifies the detached signature with gpgv and extracts a signed AArch64
Arch Linux ARM userspace archive into a new or empty directory. This does
not build a CP20S image, install a kernel, partition storage, or flash a device.
Run as root so archive ownership and permissions can be preserved.
EOF
}

if [[ $# -ne 4 ]]; then usage; exit 2; fi
archive=$(realpath -e -- "$1")
signature=$(realpath -e -- "$2")
keyring=$(realpath -e -- "$3")
destination=$4

for tool in gpgv sha256sum tar realpath find; do
  command -v "$tool" >/dev/null || { echo "Missing required tool: $tool" >&2; exit 1; }
done
[[ $EUID -eq 0 ]] || { echo "Run as root to preserve rootfs ownership and modes." >&2; exit 1; }
[[ -f $archive && -f $signature && -f $keyring ]] || { echo "Archive, signature, and keyring must be regular files." >&2; exit 1; }
[[ ! -L $destination ]] || { echo "Refusing a symlink destination." >&2; exit 1; }

parent=$(realpath -e -- "$(dirname -- "$destination")")
leaf=$(basename -- "$destination")
destination="$parent/$leaf"
[[ $destination != / && $destination != /usr && $destination != /etc && $destination != /var ]] || {
  echo "Refusing a system directory as the destination." >&2; exit 1;
}
if [[ -e $destination ]]; then
  [[ -d $destination ]] || { echo "Destination exists and is not a directory." >&2; exit 1; }
  [[ -z $(find "$destination" -mindepth 1 -maxdepth 1 -print -quit) ]] || {
    echo "Destination must be empty: $destination" >&2; exit 1;
  }
else
  mkdir -- "$destination"
fi

echo "Verifying detached signature..."
gpgv --keyring "$keyring" "$signature" "$archive"
echo "Verified archive SHA-256: $(sha256sum "$archive" | awk '{print $1}')"
echo "Extracting signed generic AArch64 userspace to $destination"
tar --extract --file "$archive" --directory "$destination" \
  --numeric-owner --same-owner --same-permissions --xattrs --acls
echo "Extraction complete. This tree is not CP20S-bootable by itself."
