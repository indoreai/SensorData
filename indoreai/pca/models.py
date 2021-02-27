from datetime import datetime
from indoreai import db, login_manager


class Samples(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Sample = db.Column(db.Integer, nullable=False)
    HRBME680 = db.Column(db.Integer, nullable=False)
    RBME680 = db.Column(db.Integer, nullable=False)
    CO2SGP30 = db.Column(db.Integer, nullable=False)
    TVOCSGP30 = db.Column(db.Integer, nullable=False)
    H2SGP30 = db.Column(db.Integer, nullable=False)
    EtanolSGP30 = db.Column(db.Integer, nullable=False)


    @classmethod
    def get_entities_sensor(cls, attr):
        return getattr(cls, attr) 
        

class Samples_meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    device_name = db.Column(db.String(256), nullable=True)
    sample_set_id = db.Column(db.String(256), nullable=True)
    name = db.Column(db.String(256), nullable=True)
    sample_date = db.Column(db.String(256), nullable=True)
    start_sample_id = db.Column(db.Integer, nullable=True)
    end_sample_id = db.Column(db.Integer, nullable=True)
    filename = db.Column(db.String(256), nullable=True)
    no_of_record = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Samples_userdevices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    device_name = db.Column(db.String(256), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Sample('{self.id}', '{self.user_id}', '{self.device_name}'," \
               f"'{self.date_created}')"
