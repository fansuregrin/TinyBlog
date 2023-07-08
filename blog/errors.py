from flask import render_template

from . import blog
from utils.utils import get_option_value


@blog.errorhandler(404)
def page_not_found(e):
    return render_template('blog/404.html', blog_title=get_option_value('title')), 404

@blog.errorhandler(403)
def forbidden(e):
    return render_template('blog/403.html', blog_title=get_option_value('title')), 403