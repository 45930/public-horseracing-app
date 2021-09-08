from .base import Base

from app.db import db


class Horse(Base):
    __tablename__ = 'horses'
    __table_args__ = (
        None,
        db.UniqueConstraint(
            'name',
            'year_born',
            'location_born',
            name='uniq_horse_name'
        )
    )

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    results = db.relationship("Result", back_populates="horse")
    past_performances = db.relationship(
        "PastPerformance", back_populates="horse")

    name = db.Column(db.String)
    sex = db.Column(db.String)
    year_born = db.Column(db.Integer)
    month_born = db.Column(db.Integer)
    location_born = db.Column(db.String)
    breeder = db.Column(db.String)
    color = db.Column(db.String)
    sire = db.Column(db.String)
    sire_sire = db.Column(db.String)
    dam = db.Column(db.String)
    dam_sire = db.Column(db.String)
    sale_location = db.Column(db.String)
    sale_year = db.Column(db.Integer)
    sale_price = db.Column(db.DECIMAL)
    stud_fee = db.Column(db.DECIMAL)

    def __repr__(self):
        return "<Horse(name='%s')>" % (
            self.name)
