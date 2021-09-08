from .base import Base

from app.db import db


class Track(Base):
    __tablename__ = 'tracks'
    __table_args__ = (
        db.Index(
            'code_index',
            'code'
        ),
        db.UniqueConstraint(
            'code',
            name='uniq_code'
        )
    )

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    races = db.relationship("Race", back_populates="track")
    courses = db.relationship("Course", back_populates='track')

    code = db.Column(db.String)
    name = db.Column(db.String)
    state = db.Column(db.String)

    def __repr__(self):
        return "<Track(code='%s')>" % (self.code)
