import os

from flask.ext.script import Manager

from app import app
from app.utils import get_valid_publish_key


manager = Manager(app)


def get_and_validate(field_name, is_bool=False):
    value = ''
    while not value:
        value = input('{} >> '.format(field_name)).strip()
        if is_bool:
            value = value.lower()
            if value not in ('true', 'false'):
                print('Please enter True or False')
                value = ''
            else:
                return value == 'true'
    return value


@manager.command
def runserver():
    app.run(debug=True, port=8888)


@manager.command
def pubkey(data_file):
    secret_key = os.environ.get('SECRET_KEY')
    publish_key = get_valid_publish_key(data_file.strip(), secret_key)
    print(publish_key)


if __name__ == '__main__':
    manager.run()

