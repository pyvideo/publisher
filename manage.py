from flask.ext.script import Manager

from app import app


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


if __name__ == '__main__':
    manager.run()

