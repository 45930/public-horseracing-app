from .base import Base

from app.db import db


class Trainer(Base):
    __tablename__ = 'trainers'
    __table_args__ = (
        None,
        db.UniqueConstraint(
            'full_name',
            name='uniq_trainer'
        )
    )

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    results = db.relationship("Result", back_populates="trainer")

    full_name = db.Column(db.String)

    def __repr__(self):
        return "<Trainer(name='%s')>" % (
            self.full_name)
