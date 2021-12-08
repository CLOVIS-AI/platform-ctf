from ..extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from sqlalchemy import func


class Documentation(db.Model):
    """Base Challenge class."""

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    short_name = Column(String(8), unique=True, nullable=False)
    description = Column(String(1024000), default="A compléter")
    category = Column(String(32), default="Misc")
    author = Column(String(64), default="Anonymous")
