import hashlib
import json
import os
import shutil
import subprocess

import celery as celery_lib
import raven
from raven.contrib.celery import register_signal, register_logger_signal

from . import app


WORKING_DIR = '/tmp/pytube'
REPO_URL = 'git@github.com:pytube/pytube.git'


sentry_dsn = app.config.get('SENTRY_DSN')
if sentry_dsn:
    class Celery(celery_lib.Celery):
    
        def on_configure(self):
            client = raven.Client(sentry_dsn)
    
            # register a custom filter to filter out duplicate logs
            register_logger_signal(client)
    
            # hook into the Celery error handler
            register_signal(client)
else:
    Celery = celery_lib.Celery


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)


def subproc(args, timeout=10):
    ret = subprocess.Popen(args, cwd=WORKING_DIR).wait(timeout=timeout)
    if ret:
        raise ValueError('Got retrun code {} from executing {}'.format(ret, args))


@celery.task
def publish_media_record(data_file):
    """
    Publish a media request.
    """
    # ensure working area is set
    if os.path.exists(os.path.join(WORKING_DIR, '.git')): 
        subproc(('/usr/bin/git', 'checkout', 'master'))
        subproc(('/usr/bin/git', 'reset', 'HEAD', '--hard'))
        subproc(('/usr/bin/git', 'pull', 'origin', 'master'), timeout=30)

    else:
        subproc(('/usr/bin/git', 'clone', REPO_URL), timeout=60)

    # create new branch
    m = hashlib.md5()
    m.update(data_file.encode())
    digest = m.hexdigest()

    subproc(('/usr/bin/git', 'checkout', '-b', digest))

    # find file in data
    abs_data_file_path = os.path.join(WORKING_DIR, data_file)
    if not os.path.exists(abs_data_file_path):
        raise RuntimeError('No file at path: {}'.format(abs_data_file_path))

    # de-serialize file
    with open(abs_data_file_path) as fp:
        data = json.load(fp)
 
    # check that talk is not already published
    if data['status'] == 'published':
        return

    # update media record file with status: published
    data['status'] = 'published'

    with open(abs_data_file_path, 'w') as fp:
        json.dump(data, fp)

    subproc(('/usr/bin/git', 'add', data_file))

    # commit changes
    subproc(('/usr/bin/git', 'commit', '-m', 'Publish {}'.format(digest)))

    # merge new branch into master
    subproc(('/usr/bin/git', 'checkout', 'master'))
    subproc(('/usr/bin/git', 'merge', digest))

    # delete feature branch
    subproc(('/usr/bin/git', 'branch', '-D', digest))

    # push to master
    subproc(('/usr/bin/git', 'push', 'origin', 'master'))

