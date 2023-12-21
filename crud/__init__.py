from .crud_base import CRUDBase
from .crud_user import CRUDUser
from .crud_email import CRUDEmail
from db import models


user = CRUDUser(models.User)
email = CRUDEmail(models.Email)
