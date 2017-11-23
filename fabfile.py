import sys

from fabric.api import run, env, local, sudo, prefix, task, cd
from fabric.operations import put
from fabric.context_managers import shell_env

# run production deploy with command "fab prod deploy"
# run qa deploy with command "fab test deploy"

env.path = '/home/env3/sockets'


def clean():
    with cd(env.path):
        run('find . -name "*.pyc" -exec rm -f {} \;')


@task
def restart():
    sudo('service apache2 restart')


@task
def update():
    with cd(env.path):
        # run('git checkout {}'.format(env.branch))
        run('git stash')
        run('git pull origin {}'.format(env.branch))
        with prefix('source /home/env3/bin/activate'):
        # with shell_env(DJANGO_CONFIGURATION='{}'.format(env.config)):
            run('pip install -r requirements.txt')
            run('python manage.py migrate')
            # run('python manage.py collectstatic --noinput')
    # for logs permission fix
    sudo('service apache2 restart')


@task
def deploy():
    """ Update and restart """
    clean()
    update()
    restart()


@task
def prod():
    env.hosts = ['185.69.154.160']
    env.branch = 'master'
    env.user = 'root'
    # env.key_filename = ["~/.ssh/id_rsa", ]
    env.path = '/home/env2/sockets'
