from flask import Flask


def create_app(name: str, config=None):
    """A simple factory function to create an app.
    :param name: the name of the app.
    :param type: `str`
    :param config: a config object or class.
    :param type: `BaseConfig` or others
    :return: a Flask app.
    :rtype: `Flask`
    """
    app = Flask(name)
    if config:
        app.config.from_object(config)
    return app