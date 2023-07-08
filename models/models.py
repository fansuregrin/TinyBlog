import time
from datetime import datetime
from flask_security import UserMixin, RoleMixin

from converter import create_converter
from . import db
from .utils import slugify, html_to_text


posts_tags = db.Table('posts_tags', 
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

roles_users = db.Table('roles_users',
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

posts_users = db.Table('posts_users',
                       db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True)
    text = db.Column(db.Text)
    text_type_id = db.Column('text_type', db.Integer, db.ForeignKey('text_type.id'), nullable=False)
    category_id = db.Column('category', db.Integer, db.ForeignKey('category.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    tags = db.relationship('Tag', secondary=posts_tags,
                           backref=db.backref('posts'), lazy='immediate')
    authors = db.relationship('User', secondary=posts_users,
                              backref=db.backref('posts'), lazy='select')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate_slug()

    def validate_slug(self):
        if not self.slug or self.slug.isspace():
            if self.title or self.title == '':
                self.slug = slugify(self.title)
            else:
                self.slug = str(int(time.time()))
        else:
            self.slug = slugify(self.slug)
    
    def convert_text(self):
        text_converter = create_converter(self.text_type_id)
        return text_converter.convert_to_html(self.text)

    def __repr__(self):
        return f'<Post id: {self.id}, title: {self.title}>'
    
    @staticmethod
    def get_time(datetime_obj, format='%Y-%m-%d'):
        return datetime_obj.strftime(format)
    
    def get_summary(self):
        html = self.convert_text()
        plain_text = html_to_text(html)
        limited_num = 80
        if len(plain_text) > limited_num:
            summary = plain_text[0:limited_num] + '...'
        else:
            summary = plain_text
        return  summary
    

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    slug = db.Column(db.String(120), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate_slug()

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<Tag id: {self.id}, name: {self.name}>'
    
    def validate_slug(self):
        if not self.slug or self.slug.isspace():
            if self.name or self.name == '':
                self.slug = slugify(self.name)
            else:
                self.slug = str(int(time.time()))
        else:
            self.slug = slugify(self.slug)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    slug = db.Column(db.String(120), unique=True)
    posts = db.relationship('Post', backref='category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate_slug()

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<Tag id: {self.id}, name: {self.name}>'
    
    def validate_slug(self):
        if not self.slug or self.slug.isspace():
            if self.name or self.name == '':
                self.slug = slugify(self.name)
            else:
                self.slug = str(int(time.time()))
        else:
            self.slug = slugify(self.slug)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users'))
    
    def __repr__(self):
        return f'<User id: {self.id}, name: {self.name}>'
    
    def __str__(self):
        return f'{self.name}'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f'<Role id: {self.id}, name: {self.name}>'
    
    def __str__(self):
        return f'{self.name}'


class TextType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    posts = db.relationship('Post', backref='text_type')

    def __repr__(self):
        return f'<TextType id: {self.id}, name: {self.name}>'
    
    def __str__(self):
        return f'{self.name}'


class Option(db.Model):
    name = db.Column(db.String(100))
    value = db.Column(db.String(300))

    __table_args = (db.PrimaryKeyConstraint(name, name='pk_option'),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __repr__(self):
        return f'<Option: {self.name} {self.value}>'