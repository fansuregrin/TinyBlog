from flask_sqlalchemy import SQLAlchemy

from .config import metadata


db = SQLAlchemy(metadata=metadata)

from .models import (
    Post,
    Tag,
    Category,
    User,
    Role,
    TextType,
    Option
)
__all__ = [Post, Tag, Category, User, Role, TextType, Option]