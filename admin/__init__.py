from flask_admin import Admin

from .views import (
    HomeAdminView, PostAdminView,
    TagAdminView, UserAdminView, CategoryAdminView,
    OptionGeneralAdminView
)
from models import db
from models import User, Post, Tag, Option, Category


admin = Admin(name='TinyBlog', endpoint='admin', index_view=HomeAdminView(name='DashBoard', template='admin/index.html'),
              template_mode='bootstrap4', base_template='admin/my_master.html')

admin.add_view(PostAdminView(Post, db.session, category='Manage'))
admin.add_view(TagAdminView(Tag, db.session, category='Manage'))
admin.add_view(CategoryAdminView(Category, db.session, category='Manage'))
admin.add_view(UserAdminView(User, db.session, category='Manage'))
admin.add_view(OptionGeneralAdminView(Option, db.session, category='Settings'))
