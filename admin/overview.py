from abc import ABC, abstractmethod
from flask import render_template

from models import db, Post, Category, Tag, User


class OverviewProducer:
    def __init__(self, overview) -> None:
        self.__overview = overview

    def set_overview(self, overview):
        self.__overview = overview

    def produce_overview_info(self) -> str:
        return self.__overview.render_info()
    

class Overview(ABC):
    @abstractmethod
    def render_info(self) -> str:
        pass


class PostOverview(Overview):
    def render_info(self) -> str:
        count = db.session.query(Post).count()
        recent_posts_count = 5
        recent_posts = db.session.execute(db.select(Post)).scalars().fetchmany(recent_posts_count)
        return render_template('admin/post_overview.html', posts=recent_posts, count=count)
    

class CategoryOverview(Overview):
    def render_info(self) -> str:
        categories = db.session.execute(db.select(Category)).scalars().all()
        return render_template('admin/category_overview.html', categories=categories)
    

class TagOverview(Overview):
    def render_info(self) -> str:
        tags = db.session.execute(db.select(Tag)).scalars().all()
        return render_template('admin/tag_overview.html', tags=tags)

class UserOverview(Overview):
    def render_info(self) -> str:
        users = db.session.execute(db.select(User)).scalars().all()
        return render_template('admin/user_overview.html', users=users)