from .base import Base

from app.db import db


class PastPerformance(Base):
    __tablename__ = 'past_performances'
    __table_args__ = (
        db.Index(
            '_horse_track_date',
            'horse_id',
            'track_code',
            'race_date'
        ),
        db.UniqueConstraint(
            'horse_id',
            'track_code',
            'race_date',
            name='uniq_horse_track_date'
        )
    )

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id'))
    horse = db.relationship("Horse", back_populates="past_performances")

    horse_name = db.Column(db.String)
    foreign_or_domestic = db.Column(db.String)
    foreign_race = db.Column(db.String)
    race_date = db.Column(db.Date)
    track_code = db.Column(db.String)
    race_number = db.Column(db.Integer)
    surface = db.Column(db.String)
    timeform_code = db.Column(db.String)
    inner_track_code = db.Column(db.String)
    distance = db.Column(db.DECIMAL)
    race_class = db.Column(db.String)
    claim_price = db.Column(db.DECIMAL)
    purse = db.Column(db.DECIMAL)
    track_condition = db.Column(db.String)
    sex_restrictions = db.Column(db.String)
    age_restrictions = db.Column(db.String)
    state_bred = db.Column(db.String)
    field_size = db.Column(db.Integer)
    first_fraction = db.Column(db.DECIMAL)
    second_fraction = db.Column(db.DECIMAL)
    third_fraction = db.Column(db.DECIMAL)
    fourth_fraction = db.Column(db.DECIMAL)
    fifth_fraction = db.Column(db.DECIMAL)
    sixth_fraction = db.Column(db.DECIMAL)
    final_time = db.Column(db.DECIMAL)
    first_horse = db.Column(db.String)
    second_horse = db.Column(db.String)
    third_horse = db.Column(db.String)
    grade = db.Column(db.Integer)
    post_position = db.Column(db.Integer)
    first_call_position = db.Column(db.Integer)
    first_call_lengths_back = db.Column(db.DECIMAL)
    first_call_position = db.Column(db.Integer)
    first_call_lengths_back = db.Column(db.DECIMAL)
    first_call_position = db.Column(db.Integer)
    first_call_lengths_back = db.Column(db.DECIMAL)
    second_call_position = db.Column(db.Integer)
    second_call_lengths_back = db.Column(db.DECIMAL)
    third_call_position = db.Column(db.Integer)
    third_call_lengths_back = db.Column(db.DECIMAL)
    fourth_call_position = db.Column(db.Integer)
    fourth_call_lengths_back = db.Column(db.DECIMAL)
    stretch_call_position = db.Column(db.Integer)
    stretch_call_lengths_back = db.Column(db.DECIMAL)
    final_call_position = db.Column(db.Integer)
    final_call_lengths_back = db.Column(db.DECIMAL)
    beyer_or_foreign_speed = db.Column(db.Integer)
    comment = db.Column(db.String)
    odds = db.Column(db.DECIMAL)
    odds_position = db.Column(db.Integer)
    claimed_code = db.Column(db.String)
    lasix = db.Column(db.String)
    bute = db.Column(db.String)
    blinkers = db.Column(db.String)
    bandages = db.Column(db.String)
    jockey = db.Column(db.String)
    trainer = db.Column(db.String)
    track_variant = db.Column(db.Integer)
    speed_rating = db.Column(db.Integer)
    breed = db.Column(db.String)
    owner = db.Column(db.String)

    def __repr__(self):
        return "<PastPerformance(id='%s' horse_id='%s')>" % (
            self.id, self.horse_id)
