from tortoise import run_async
from tortoise import Tortoise

import security
from db.models import User, Email
from db.database import db_conn_str


async def create_admin():
    await Tortoise.init(db_url=db_conn_str, modules={"models": ["db.models"]})
    await Tortoise.generate_schemas()

    admin_data = {
        'email': 'ad@min.ru',
        'username': 'admin',
        'password_hash': security.get_password_hash('admin'),
        'is_active': True,
        'is_superuser': True
    }
    user = await User.create(username=admin_data['username'],
                             password_hash=admin_data['password_hash'],
                             is_active=admin_data['is_active'],
                             is_superuser=admin_data['is_superuser'])
    await Email.create(email=admin_data['email'], is_prime=True, user=user)


run_async(create_admin())
