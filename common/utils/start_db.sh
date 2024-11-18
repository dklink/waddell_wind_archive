parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
source "$parent_path"/../../.env
pg_isready || pg_ctl start -D "$DB_DATA_DIR" -l "$DB_LOGFILE"
