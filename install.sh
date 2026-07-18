#!/usr/bin/env bash
# install.sh — symlink a 365Skill skill into agent clients' skill directories.
#
# Usage:
#   ./install.sh <skill-id>                 install into all detected clients
#   ./install.sh <skill-id> claude kimi     install into selected clients
#   ./install.sh --list                     list skills in this repo
#
# Detected clients and their skill roots:
#   claude → ~/.claude/skills
#   codex  → ~/.codex/skills
#   kimi   → ~/Library/Application Support/kimi-desktop/daimon-share/daimon/skills
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIMI_ROOT="$HOME/Library/Application Support/kimi-desktop/daimon-share/daimon/skills"

client_root() {
  case "$1" in
    claude) echo "$HOME/.claude/skills" ;;
    codex)  echo "$HOME/.codex/skills" ;;
    kimi)   echo "$KIMI_ROOT" ;;
    *) return 1 ;;
  esac
}

if [[ "${1:-}" == "--list" ]]; then
  ls "$REPO_ROOT/skills"
  exit 0
fi

SKILL_ID="${1:-}"
if [[ -z "$SKILL_ID" ]]; then
  sed -n '1,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 2
fi

SRC="$REPO_ROOT/skills/$SKILL_ID"
if [[ ! -f "$SRC/SKILL.md" ]]; then
  echo "error: $SRC/SKILL.md not found (run ./install.sh --list to see available skills)" >&2
  exit 1
fi

if [[ $# -ge 2 ]]; then
  CLIENTS=("${@:2}")
else
  CLIENTS=(claude codex kimi)
fi

installed=0
for client in "${CLIENTS[@]}"; do
  root="$(client_root "$client")" || { echo "skip: unknown client '$client'"; continue; }
  if [[ ! -d "$root" ]]; then
    parent="$(dirname "$root")"
    if [[ -d "$parent" ]]; then
      mkdir -p "$root"
    else
      echo "skip: $client not detected ($root)"
      continue
    fi
  fi
  dest="$root/$SKILL_ID"
  if [[ -L "$dest" && "$(readlink "$dest")" == "$SRC" ]]; then
    echo "ok:   $client → already linked"
  elif [[ -e "$dest" || -L "$dest" ]]; then
    echo "skip: $client → $dest exists (not our symlink; remove it manually to relink)"
    continue
  else
    ln -s "$SRC" "$dest"
    echo "ok:   $client → $dest"
  fi
  installed=$((installed + 1))
done

echo "done: $SKILL_ID installed into $installed client(s)"
