from geoalchemy2.types import Geography, Geometry
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import func
from sqlalchemy.sql import cast

from app import db


class Position(db.Model):
    __table_args__ = (PrimaryKeyConstraint('location', 'operator_code'), {})
    # The SRID = 4326 is the ID of WGS84 projection
    SRS_WGS_84 = 4326
    location = db.Column(Geometry(geometry_type='POINT', srid=SRS_WGS_84), nullable=False)
    operator_code = db.Column(db.Integer, db.ForeignKey('operator.mcc_mnc'), nullable=False)
    has_2g = db.Column(db.Boolean, default=False)
    has_3g = db.Column(db.Boolean, default=False)
    has_4g = db.Column(db.Boolean, default=False)

    @classmethod
    def within_distance_func(cls, position, distance):
        """
        Creates the geoalchemy function that determines if a point is in range < distance from the position item
        :param position: the position to check distance with
        :param distance: the maximum distance in meters
        :return: function to apply to query 
        """
        point = func.ST_GeomFromText('POINT({0} {1})'.format(*position), srid=Position.SRS_WGS_84)
        return func.ST_DWithin(cast(Position.location, Geography(srid=Position.SRS_WGS_84)), point, distance)

    def __repr__(self):
        return '<Position {} - Op {} - 2G {} - 3G {} - 4G {} >'.format(self.location, self.operator_code,
                                                                       self.has_2g, self.has_3g, self.has_4g)
