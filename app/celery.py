import celery as celery_lib
import raven
from raven.contrib.celery import register_signal, register_logger_signal

from . import app


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


@celery.task
def publish_media_record(data_file, category_slug, media_record_slug):
    """
    Publish a media request.
    """
    print(locals())
    # check working area is clean

    # clone repo

    # find file in data

    # de-serialize file

    # find media record slug

    # check that talk is not already published

    # update media record file with status: published

    # make new branch

    # merge new branch into master

    # push to master

    # clean up working area

