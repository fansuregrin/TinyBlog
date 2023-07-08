from app import create_app
from config import BaseConfig
from utils.utils import is_installed


if not is_installed():
    from install import install
    app = create_app('tinyblog', BaseConfig)
    app.register_blueprint(install)
else:
    import json
    class ConfigWithDb(BaseConfig):
        with open('db_config.json') as f:
            db_config = json.load(f)
        SQLALCHEMY_DATABASE_URI = db_config['SQLALCHEMY_DATABASE_URI']
    from models import db
    app = create_app('tinyblog', ConfigWithDb)
    db.init_app(app)
    from blog import blog
    app.register_blueprint(blog)
    from admin import admin
    admin.init_app(app)
    from security import security, user_datastore
    security.init_app(app, user_datastore)


if __name__ == '__main__':
    app.run() # this line only can be used in development mode.
    
    # from waitress import serve
    # serve(app, host='127.0.0.1', port=5000)