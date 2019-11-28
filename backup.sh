#!/bin/bash
echo "MIS Application Backup under process......Please wait!!!!!"
tar czf "misappbackup_$(date '+%d%m%y').tar.gz" --absolute-names /var/www
echo "MIS Application backup is completed. Now MIS database backup is under process.... Please wait!!!"

