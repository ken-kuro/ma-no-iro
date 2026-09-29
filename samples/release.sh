#!/usr/bin/env bash
# Tag a palette release once derive.py agrees with palette.json.
set -euo pipefail

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
version="${1:?usage: release.sh <version>}"

log() { printf '\033[2m%s\033[0m %s\n' "$(date +%H:%M:%S)" "$*" >&2; }

if ! python3 "$ROOT/tools/derive.py" --check >/dev/null; then
  log "palette.json is stale or breaks policy"
  exit 1
fi

case "$version" in
  [0-9]*.[0-9]*.[0-9]*) ;;
  *) log "not a version: $version"; exit 2 ;;
esac

for flavor in kuromurasaki byakuroku; do
  count=$(grep -c "\"$flavor\"" "$ROOT/palette.json" || true)
  log "$flavor: ${count} mentions"
done

git -C "$ROOT" tag -a "v$version" -m "Ma no Iro $version" && log "tagged v$version"
export MA_NO_IRO_VERSION=$version
