import os
from fabric.api import *

env.hosts = "192.168.1.168"
env.user = 'u'
env.password = 'a'

os.path.abspath('.')


def _copy_ssh_key():
    pwd = os.path.abspath('.')
    put(os.path.join(pwd, 'Deploy/ssh/id_rsa'),
        '/home/u/.ssh/',mode='0600', use_sudo=True)
    put(os.path.join(pwd, 'Deploy/ssh/id_rsa.pub'),
        '/home/u/.ssh/',mode='0644', use_sudo=True)
    run('ssh -T git@gitee.com')


def _install_software():
    """
    ### 安装redis postgres nginx
    """
    sudo('apt-get install redis-server postgresql-9.5 nginx python3')


def _create_db_and_dbuser():
    """
    ### 创建数据库用户和数据库
    """
    print('创键数据库用户,并填写密码')
    run(r"su postgres -c 'createuser -U postgres -s -l -P dev'")
    print('创键数据库')
    run(r"su postgres -c 'createdb dev'")


def clear_db_and_dbuser():
    """
    ### 删除数据库用户和数据库
    """
    run('rm -rf /home/u/fabtest')
    run(r"su postgres -c 'dropdb dev'")
    run(r"su postgres -c 'dropuser dev'")


def _nginx_config():
    """
    # 配置nginx
    """
    pwd = os.path.abspath('.')
    put(os.path.join(pwd, 'Deploy/nginx/default'),
        '/etc/nginx/sites-available/', mode='0644', use_sudo=True)
    sudo('chown root:root /etc/nginx/sites-available/default')


def _init_web_server():
    """
    ### 初始化后台代码
    """
    with cd('/home/u/fabtest'):
        print('克隆web后台代码')
        run('git clone git@gitee.com:lambda_project/Lambda.git')
    with cd('/home/u/fabtest/Lambda'):
        print('安装python包')
        sudo('pip3 install -r requirements.txt')
        print('切换分支到年报')
        run('git checkout feature-annual-report')
        print('创建migrations')
        run('rm -rf AnnualReport/migrations')
        run('rm -rf project/migrations')
        run('rm -rf hy_report/migrations')
        run('python3 manage.py makemigrations AnnualReport')
        run('python3 manage.py makemigrations project')
        run('python3 manage.py makemigrations hy_report')
        run('python3 manage.py makemigrations')
    with cd('/home/u/fabtest/Lambda'):
        print('初始化表结构')
        run('python3 manage.py migrate')
    with cd('/home/u/fabtest/Lambda/InitData/dump'):
        print('导入初始化数据')
        run(r"su postgres -c 'psql -d dev < restore_db_data.psql'")


def _init_web_front():
    """
    ### 初始化前端代码
    """
    with cd('/home/u/fabtest'):
        print('克隆前端代码')
        run('git clone git@gitee.com:lambda_project/lambdafrontend.git')
    with cd('/home/u/fabtest/lambdafrontend'):
        print('切换分支到年报')
        run('git checkout annual-report')
        print('安装npm包')
        run('npm install')


def runserver():
    """
    ### 启动后台服务
    """
    with cd('/home/u/fabtest/Lambda'):
        run('python3 manage.py runserver &')


def runfront():
    """
    ### 启动前端服务服务
    """
    with cd('/home/u/fabtest/lambdafrontend'):
        run('npm start &')


def deploy():
    _install_software()
    _nginx_config()
    _copy_ssh_key()
    _create_db_and_dbuser()

    print('创建项目目录')
    run('mkdir /home/u/fabtest')
    _init_web_server()
    _init_web_front()
    runserver()
    runfront()
