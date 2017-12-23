if [ "$1" == "DEBUG" ]; then
    echo "In Development Environment"
    export DEBUG=1
else
    echo "In Production Environment"
    export DJANGO_STATIC_ROOT=$1
    export IS_ADMIN=$2
    export DB_PATH=$3
fi

cd core

# Migrate 
python manage.py migrate
python manage.py makemigrations core_settings
python manage.py migrate core_settings
python manage.py makemigrations users
python manage.py migrate users

# Initialize Basic Data
python manage.py initdata country
python manage.py initdata bank
python manage.py initdata province_cn
python manage.py initdata fund_limit
python manage.py initdata kyc_level
python manage.py initdata point_level
python manage.py initdata languages
python manage.py init_super_user admin

# Generate Translation Files
django-admin compilemessages -l zh_Hans
django-admin compilemessages -l ja_Jp

# sudo yum install iptables-services
# sudo systemctl enable iptables
# sudo iptables -A INPUT -p tcp --dport 23212 -s 47.88.193.163 -j ACCEPT
# sudo iptables -A INPUT -p tcp --dport 23212 -j DROP
# sudo iptables -A INPUT -p tcp --dport 23213 -s 10.26.59.67 -j ACCEPT
# sudo iptables -A INPUT -p tcp --dport 23213 -j DROP
# sudo /usr/libexec/iptables/iptables.init save
