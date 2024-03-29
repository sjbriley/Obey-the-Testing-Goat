import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/sjbriley/to_do.git'

def deploy():
    # env.user is signed in user, env.host is address of server from command line
    # env.host: /www.mydjangoproject.xyz/to_do/
    site_folder = '/home/sam/django/to_do'#.format(env.user, env.host)
    print('site_folder: ' + site_folder)
    #run(f'mkdir -p {site_folder}')
    with cd(site_folder): # run these commands inside this directory
        _get_latest_source()
        print('ran _get_latest_source')
        _update_virtualenv()
        print('_update_virtualenv')
        _create_or_update_dotenv()
        print('ran _create_or_update_dotenv')
        _update_static_files()
        print('ran _update_static_files')
        _update_database()
        print('ran _update_database')

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")

def _update_virtualenv():
    if not exists("virtualenv/bin/pip"):
        run(f"python3 -m venv virtualenv")
    run("./virtualenv/bin/pip install -r requirements.txt")

def _create_or_update_dotenv():
    append(".env", "DJANGO_DEBUG_FALSE=y")
    append(".env", f"SITENAME=.mydjangoproject.xyz")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = "".join(random.SystemRandom().choices('abcdefghijklmnopqrestuvwxyz0123456789', k=50))
        append(".env", f"DJANGO_SECRET_KEY={new_secret}")

def _update_static_files():
    run("./virtualenv/bin/python3 manage.py collectstatic --noinput")

def _update_database():
    run("./virtualenv/bin/python3 manage.py migrate --noinput")

if __name__=='__main__':
    deploy()