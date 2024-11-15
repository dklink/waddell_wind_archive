source .env
pg_isready && pg_ctl stop -D "$DB_DATA_DIR" -l "$DB_LOGFILE"
