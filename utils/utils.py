import os
import json
import random
import string
import uuid
import re
import sqlalchemy as sa
import sqlalchemy.orm as saorm

from models import db
from models.models import Option, User, Role, TextType


BASE_DIR = os.path.dirname(os.path.abspath(__name__))


def is_valid_username(username):
    if len(username) < 1:
        return False
    if any(char.isspace() for char in username):
        return False
    return True

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    if len(password) < 6:
        return False
    characters = string.ascii_letters + string.digits + string.punctuation
    if all(char in characters for char in password):
        return True
    else:
        return False

def get_option_value(option_name):
    option = db.session.execute(db.select(Option).filter_by(name=option_name)).scalar()
    return option.value

def is_installed():
    if os.path.exists('db_config.json'):
        try:
            # read database configuration
            with open('db_config.json') as f:
                db_config = json.load(f)
            db_uri = db_config['SQLALCHEMY_DATABASE_URI']
            # connect to database to get value of teh `installed` flag
            engine = sa.create_engine(db_uri)
            session = saorm.Session(bind=engine)
            installed = session.execute(sa.select(Option).filter(
                Option.name == 'installed'
            )).scalar().value
            session.close_all()
            return int(installed)
        except:
            return False
    return False
    
def write_db_config(db_config):
    db_type = db_config['db_type']
    if db_type == 'sqlite3':
        db_filename = db_config['db_filename']
        if (not db_filename) or db_filename.isspace():
            db_filename = 'tinyblog.db'
        db_uri = f"sqlite:///{os.path.join(BASE_DIR, db_filename)}"
    elif db_type == 'mysql':
        db_uri = 'mysql://{user}:{passwd}@{addr}/{db_name}?charset={charset}'.format(
            user = db_config['db_username'],
            passwd = db_config['db_password'],
            addr = db_config['db_address'],
            db_name = db_config['db_name'],
            charset = db_config['db_charset']
        )
    db_config_flask = {
        'SQLALCHEMY_DATABASE_URI': db_uri,
    }
    with open(os.path.join(BASE_DIR, 'db_config.json'), 'w') as f:
        f.write(json.dumps(db_config_flask))
    engine = sa.create_engine(db_uri)
    db.metadata.create_all(engine)

def write_amdin_config(admin_config):
    username = admin_config['username']
    if not is_valid_username(username):
        raise ValueError('invalid username')
    email = admin_config['email']
    if not is_valid_email(email):
        raise ValueError('invalid email')
    password = admin_config['password']
    if not is_valid_password(password):
        characters = string.ascii_letters + string.digits + string.punctuation
        length = 8
        admin_config['password'] = ''.join(random.choice(characters) for _ in range(length))

    with open('db_config.json') as f:
        db_config = json.load(f)
    db_uri = db_config['SQLALCHEMY_DATABASE_URI']
    engine = sa.create_engine(db_uri)
    session = saorm.Session(bind=engine)
    admin_role = Role(name='admin')
    admin_user = User(
        name = admin_config['username'],
        password = admin_config['password'],
        email = admin_config['email'],
        active = True,
        fs_uniquifier = uuid.uuid4().hex
    )
    session.add(admin_role)
    session.add(admin_user)
    admin_user.roles.append(admin_role)
    session.commit()
    session.add(TextType(id=1, name='markdown'))
    session.add(TextType(id=2, name='plain_text'))
    session.add(Option(name='title', value='TinyBlog'))
    session.add(Option(name='posts_per_page', value='5'))
    session.add(Option(name='installed', value='1'))
    session.add(Option(name='favicon', value="/static/images/favicon.ico"))
    session.commit()
    session.close_all()
    return admin_config