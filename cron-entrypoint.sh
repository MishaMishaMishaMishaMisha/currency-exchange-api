#!/bin/sh
set -e
echo "START CRON WORKS $(date)" >> /var/log/cron.log 2>&1
exec cron -f