#!/bin/bash
# 매일 cron으로 실행: 그날 분량 예약 글 발행
# 사용: crontab -e 에서 예) 0 9 * * * /var/www/html/run_daily_publish.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
mkdir -p logs
LOG="$SCRIPT_DIR/logs/daily_publish.log"
echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"
python3 auto_publish_with_images.py >> "$LOG" 2>&1
