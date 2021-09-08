from .base import Base

from app.db import db


class Jockey(Base):
    __tablename__ = 'jockeys'
    __table_args__ = (
        None,
        db.UniqueConstraint(
            'full_name',
            name='uniq_jockey'
        )
    )

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    results = db.relationship("Result", back_populates="jockey")

    full_name = db.Column(db.String)

    def __repr__(self):
        return "<Jockey(name='%s')>" % (
            self.full_name)
