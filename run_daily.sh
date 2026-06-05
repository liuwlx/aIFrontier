#!/usr/bin/env bash
set -euo pipefail
HUB_DIR="/home/ubuntu/frontier-data-hub"
LOG_FILE="/var/log/frontier-daily.log"
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
cd "$HUB_DIR"
echo "=== $(TZ='Asia/Shanghai' date) START ===" | tee -a "$LOG_FILE"
python3 skills/frontier-news-digest/scripts/pipeline.py --stages 1,2 --skip-if-done 2>&1 | tee -a "$LOG_FILE"
python3 skills/frontier-news-digest/scripts/pipeline.py --stages 3 --skip-if-done 2>&1 | tee -a "$LOG_FILE"
python3 skills/frontier-news-digest/scripts/pipeline.py --stages 4,5 --skip-if-done 2>&1 | tee -a "$LOG_FILE"
git add -A
if git diff --cached --quiet 2>/dev/null; then
  echo "No changes" | tee -a "$LOG_FILE"
else
  git commit -m "chore: daily pipeline $(TZ='Asia/Shanghai' date +%Y-%m-%d) [auto]" 2>&1 | tee -a "$LOG_FILE"
  git push origin main 2>&1 | tee -a "$LOG_FILE"
fi
echo "=== $(TZ='Asia/Shanghai' date) END ===" | tee -a "$LOG_FILE"
