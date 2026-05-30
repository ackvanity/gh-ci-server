export DEPLOYPATH="/home/hepivasi/projects/ci/"
export ENV_ACTIVATE="source /home/hepivasi/virtualenv/projects/ci/3.10/bin/activate && cd /home/hepivasi/projects/ci"

shopt -s extglob
cp -r !(.git) $DEPLOYPATH
$ENV_ACTIVATE
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
ls -a
touch restart.txt