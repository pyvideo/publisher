import os


basedir = os.path.abspath(os.path.dirname(__file__))


CELERY_BROKER_URL='redis://localhost:6379',
CELERY_RESULT_BACKEND='redis://localhost:6379'


