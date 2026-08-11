#!/usr/bin/env bash
set -euo pipefail

readonly OCI_HOST="opc@138.3.208.8"
readonly OCI_KEY="${OCI_KEY:-$HOME/.key/oci.key}"
readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly TARGET_DIR="$REPO_ROOT/static/snowflake-monitor"

mkdir -p "$TARGET_DIR/features" "$TARGET_DIR/diff" "$TARGET_DIR/assets"

rsync -az --delete --exclude .DS_Store -e "ssh -o BatchMode=yes -o ConnectTimeout=10 -i $OCI_KEY" \
  "$OCI_HOST:/home/opc/snowflake-monitor-portal/site/" "$TARGET_DIR/"
rsync -az --delete --exclude .DS_Store --exclude assets -e "ssh -o BatchMode=yes -o ConnectTimeout=10 -i $OCI_KEY" \
  "$OCI_HOST:/home/opc/snowflake-feature-monitor/site/" "$TARGET_DIR/features/"
rsync -az --delete --exclude .DS_Store -e "ssh -o BatchMode=yes -o ConnectTimeout=10 -i $OCI_KEY" \
  "$OCI_HOST:/home/opc/snowflake-feature-monitor/site/assets/" "$TARGET_DIR/assets/"
rsync -az --delete --exclude .DS_Store -e "ssh -o BatchMode=yes -o ConnectTimeout=10 -i $OCI_KEY" \
  "$OCI_HOST:/home/opc/snowflake-docs-diff/site/" "$TARGET_DIR/diff/"

"$REPO_ROOT/scripts/process_snowflake_monitor.sh" "$TARGET_DIR"

echo "Synced Snowflake monitor to $TARGET_DIR"
