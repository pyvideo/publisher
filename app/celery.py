from celery import Celery

from . import app


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
def publish_media_record(data_file, category_slug, slug):
    """
    Publish a media request.
    """
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

