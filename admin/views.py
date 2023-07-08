import uuid
from sqlalchemy import func, not_
from flask import request, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from .overview import (
    OverviewProducer, PostOverview,
    CategoryOverview, UserOverview,
    TagOverview
)
from .config import MY_DEFAULT_FORMATTERS


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass
    

class HomeAdminView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', overview_info_list=self.get_overview_info())
    
    def get_overview_info(self) -> str:
        post_overview = PostOverview()
        category_overview = CategoryOverview()
        user_overview = UserOverview()
        tag_overview = TagOverview()
        overview_producers = (
            OverviewProducer(post_overview),
            OverviewProducer(category_overview),
            OverviewProducer(user_overview),
            OverviewProducer(tag_overview)
        )
        overview_info_list = []
        for i in range(0, len(overview_producers), 2):
            overview_info_pair = '\n'.join(op.produce_overview_info() for op in overview_producers[i:i+2])
            overview_info_list.append(overview_info_pair)
        return overview_info_list


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.validate_slug()
        return super().on_model_change(form, model, is_created)
    

class PostAdminView(AdminMixin, BaseModelView):
    page_size = 10
    column_list = ('title', 'authors', 'created', 'modified')
    column_labels = {
        'title': 'Title',
        'authors': 'Author(s)',
        'tags': 'Tag(s)',
        'created': 'Created Time',
        'modified': 'Modified Time',
    }
    form_columns = ('title', 'slug', 'category', 'text_type', 'text', 'tags', 'authors')
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_default_sort = ('created', True)
    

class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ('name', 'slug')


class CategoryAdminView(AdminMixin, BaseModelView):
    form_columns = ('name', 'slug')


class UserAdminView(AdminView):
    column_exclude_list = ('password', 'fs_uniquifier')
    form_columns = ('name', 'email', 'password', 'active', 'roles')
    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }

    def on_model_change(self, form, model, is_created):
        if model.fs_uniquifier is None:
            model.fs_uniquifier = uuid.uuid4().hex
        return super().on_model_change(form, model, is_created)
    

class OptionGeneralAdminView(AdminView):
    column_list = ('name', 'value')
    can_create = False
    can_delete = False
    
    def get_query(self):
        query = self.session.query(self.model) \
                .filter(not_(self.model.name=='installed'))
        return query
    
    def get_count_query(self):
        count = self.session.query(func.count('*')) \
                .select_from(self.model) \
                .filter(not_(self.model.name=='installed'))
        return count