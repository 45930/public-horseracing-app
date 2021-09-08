from .base import Base

from app.db import db


class Course(Base):
    __tablename__ = 'courses'
    __table_args__ = (
        db.Index(
            'track_code_index',
            'track_code'
        ),
        db.Index(
            'distance_index',
            'distance'
        ),
        db.UniqueConstraint(
            'track_code',
            'distance',
            'surface',
            name='uniq_course'
        )
    )

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    races = db.relationship("Race", back_populates="course")
    track = db.relationship("Track", back_populates="courses")
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))

    track_code = db.Column(db.String)
    distance = db.Column(db.DECIMAL)
    surface = db.Column(db.String)

    def __repr__(self):
        return "<Track(track_code='%s', distance='%s', surface='%s')>" % (
            self.track_code, self.distance, self.surface)
