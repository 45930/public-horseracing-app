from .base import Base

from app.db import db


class Race(Base):
    __tablename__ = 'races'
    __table_args__ = (
        db.Index(
            'date_index',
            'date'
        ),
        db.UniqueConstraint(
            'track_id',
            'date',
            'race_number',
            name='uniq_track_date_rnum'
        )
    )

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))
    track = db.relationship("Track", back_populates="races")
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship("Course", back_populates="races")
    results = db.relationship("Result", back_populates="race")

    date = db.Column(db.Date)
    race_number = db.Column(db.Integer)
    is_state_bred = db.Column(db.String)
    sex_restrictions = db.Column(db.String)
    age_restrictions = db.Column(db.String)
    classification = db.Column(db.String)
    purse = db.Column(db.DECIMAL)
    claim_price = db.Column(db.DECIMAL)
    grade = db.Column(db.Integer)
    day_of_week = db.Column(db.String)
    state = db.Column(db.String)
    post_time = db.Column(db.String)
    predicted_closer_percent = db.Column(db.DECIMAL)
    predicted_pacer_percent = db.Column(db.DECIMAL)
    predicted_wire_percent = db.Column(db.DECIMAL)

    def __repr__(self):
        return "<Race(track='%s', date='%s', race_number='%s')>" % (
            self.track_id, self.date, self.race_number)
