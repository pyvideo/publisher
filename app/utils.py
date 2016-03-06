from collections import OrderedDict
import hashlib
import os


SECRET_KEY = os.environ['SECRET_KEY']
REPO_PATH = os.environ['REPO_PATH']


def is_valid_content(content):
    """
    Check that data_file is valid.
    """
    data_file = os.path.join(REPO_PATH, content['data_file'])
    exists = os.path.exists(data_file)
    return exists


def get_valid_publish_key(data_file, secret_key):
    value_string = ';'.join((data_file, secret_key))

    m = hashlib.md5()
    m.update(value_string.encode())
    digest = m.hexdigest()

    return digest    


def is_valid_publish_key(content):
    """
    Check that publish key is valid
    """
    digest = get_valid_publish_key(content['data_file'], SECRET_KEY)

    return digest == content['publish_key']

