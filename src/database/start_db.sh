source .env
pg_isready || pg_ctl start -D "$DB_DATA_DIR" -l "$DB_LOGFILE"
