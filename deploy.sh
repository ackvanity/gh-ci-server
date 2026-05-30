cp -r !(.git) $DEPLOYPATH
$ENV_ACTIVATE
pip install -r requirements.txt
python manage.py migrate