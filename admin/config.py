from datetime import datetime
from flask_admin.model import typefmt


def datetime_format(view, value):
    return value.strftime('%Y-%m-%d %H:%M:%S')

MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    datetime: datetime_format
})