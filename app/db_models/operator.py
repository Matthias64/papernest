from app import db


class Operator(db.Model):
    # Operator code : mobile country code and mobile network code concatenated
    mcc_mnc = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    positions = db.relationship('Position', backref='operator', lazy='dynamic')

    def __repr__(self):
        return '<Operator MNC {} = {}>'.format(self.mcc_mnc, self.name)
