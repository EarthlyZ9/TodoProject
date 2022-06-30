# Import all the models, so that Base has them before being
# imported by Alembic

from app.db.base_class import Base  # noqa
from app.models.address import Address  # noqa
from app.models.todo import Todo  # noqa
from app.models.user import User  # noqa
