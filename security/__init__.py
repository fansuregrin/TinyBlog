from flask_security import SQLAlchemyUserDatastore, Security

from models import db
from models.models import User, Role
from utils.utils import get_option_value


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()

@security.context_processor
def security_context_processor():
    return dict(blog_title=get_option_value('title'))