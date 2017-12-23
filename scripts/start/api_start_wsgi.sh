# arg1 = django static root path
# arg2 = admin only
# arg3 = db_path
export DJANGO_STATIC_ROOT=$1
export IS_ADMIN=$2
export DB_PATH=$3

cd core
uwsgi --ini api_uwsgi.ini
