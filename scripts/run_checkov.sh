#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR=${1:-artifacts}
REPORT_PATH="$OUTPUT_DIR/checkov_report.json"

mkdir -p "$OUTPUT_DIR"

docker run --rm \
  -v "$(pwd)":/repo \
  -w /repo \
  -v "$(pwd)/$OUTPUT_DIR":/output \
  bridgecrew/checkov:latest \
  checkov -d . --output json --output-file-path /output/checkov_report.json

echo "Checkov report saved to $REPORT_PATH"
