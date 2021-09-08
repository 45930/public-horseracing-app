from .base import Base

from app.db import db


class Owner(Base):
    __tablename__ = 'owners'
    __table_args__ = (
        None,
        db.UniqueConstraint(
            'full_name',
            name='uniq_owner'
        )
    )

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    results = db.relationship("Result", back_populates="owner")

    full_name = db.Column(db.String)

    def __repr__(self):
        return "<Owner(name='%s')>" % (
            self.full_name)
