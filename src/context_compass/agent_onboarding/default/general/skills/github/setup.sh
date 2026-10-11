#!/usr/bin/env bash
# Human-run standalone GitHub CLI Project setup (legacy helper)
# (macOS/Linux). Run this yourself in an interactive terminal with
# REPO_OWNER, REPO_NAME and PROJECT_URL in the environment or as arguments.
# PROJECT_URL is required by this helper; github_codex_plugin does not run it. It
# ensures the gh CLI is present and authenticated, refreshes
# the repo access and project write scope gh needs, verifies the
# repository resolves, then
# hands detailed preflight to check_setup.py beside this file. It creates
# nothing in the repository and stores nothing itself. Authentication happens
# through `gh auth login --web` in your browser. Never paste a token into
# chat; gh keeps it in its own credential store, and this script never prints
# tokens or writes secrets to arguments, files, or logs.
#
# Usage:
#   REPO_OWNER=octo-org REPO_NAME=my-repo PROJECT_URL=https://github.com/orgs/octo-org/projects/3 ./setup.sh
#   ./setup.sh octo-org my-repo https://github.com/orgs/octo-org/projects/3
set -euo pipefail

REPO_OWNER="${1:-${REPO_OWNER:-}}"
REPO_NAME="${2:-${REPO_NAME:-}}"
PROJECT_URL="${3:-${PROJECT_URL:-}}"
MIN_GH_VERSION="2.83.2"

fail() { echo "ERROR: $1" >&2; exit 1; }

[ -n "$REPO_OWNER" ] || fail "Repository owner is required (argument 1 or REPO_OWNER)."
[ -n "$REPO_NAME" ] || fail "Repository name is required (argument 2 or REPO_NAME)."
[ -n "$PROJECT_URL" ] || fail "GitHub Project URL is required for this standalone CLI helper (argument 3 or PROJECT_URL)."

command -v gh >/dev/null 2>&1 || fail "gh CLI not found on PATH. Install it from https://cli.github.com, then re-run this script."

GH_VERSION="$(gh --version | head -n 1)"
case "$GH_VERSION" in
  "gh version "[0-9]*.[0-9]*.[0-9]*) echo "[ok] $GH_VERSION" ;;
  *) fail "Could not parse \`gh --version\` output. Reinstall gh and retry." ;;
esac
# Numeric dotted comparison without GNU sort -V (absent on macOS BSD sort).
ver_at_least() {
  awk -v have="$1" -v floor="$2" 'BEGIN {
    split(have, h, "."); split(floor, f, ".");
    for (i = 1; i <= 3; i++) {
      if (h[i]+0 > f[i]+0) exit 0;
      if (h[i]+0 < f[i]+0) exit 1;
    }
    exit 0;
  }'
}
HAVE_VERSION="$(expr "$GH_VERSION" : 'gh version \([0-9][0-9.]*\)')"
if ver_at_least "$HAVE_VERSION" "$MIN_GH_VERSION"; then
  :
else
  echo "[warn] gh $HAVE_VERSION is older than the supported floor $MIN_GH_VERSION. Continuing anyway; check_setup.py enforces the floor." >&2
fi

if gh auth status >/dev/null 2>&1; then
  echo "[ok] gh authenticated"
else
  echo "Opening browser authentication (gh auth login --web). Complete sign-in there; no token is shown here."
  gh auth login --web || fail "gh authentication did not complete."
fi

# Refresh (never downgrade silently): repo read, org read, project write.
# Interactive when the account needs to approve; nothing secret is echoed.
gh auth refresh -s repo -s read:org -s project \
  || fail "Scope refresh did not complete. Re-run this script after reviewing the gh prompt."
echo "[ok] scopes refreshed (repo, read:org, project)"

RESOLVED="$(gh repo view "$REPO_OWNER/$REPO_NAME" --json nameWithOwner --jq '.nameWithOwner')" \
  || fail "Repository '$REPO_OWNER/$REPO_NAME' did not resolve. Check spelling and account access."
echo "[ok] repository resolves: $RESOLVED"

PYTHON=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then PYTHON="$candidate"; break; fi
done
[ -n "$PYTHON" ] || fail "No Python 3 interpreter found. Install Python 3.10+ and re-run this script."

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ARGS=("$SCRIPT_DIR/check_setup.py" --owner "$REPO_OWNER" --repo "$REPO_NAME" --project-url "$PROJECT_URL")
"$PYTHON" "${ARGS[@]}" || fail "Preflight reported a problem; see its message above."
echo "Setup preflight passed. Nothing was created, modified, or stored by this script."
