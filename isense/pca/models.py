from datetime import datetime
from isense import db, login_manager


class Samples(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Sample = db.Column(db.Integer, nullable=False)
    TempBME680 = db.Column(db.Integer, nullable=False)
    PresureBME680 = db.Column(db.Integer, nullable=False)
    HRBME680 = db.Column(db.Integer, nullable=False)
    RBME680 = db.Column(db.Integer, nullable=False)
    CO2SGP30 = db.Column(db.Integer, nullable=False)
    TVOCSGP30 = db.Column(db.Integer, nullable=False)
    H2SGP30 = db.Column(db.Integer, nullable=False)
    EtanolSGP30 = db.Column(db.Integer, nullable=False)
    CO2CCS811 = db.Column(db.Integer, nullable=False)
    TVOCCCS811 = db.Column(db.Integer, nullable=False)
    ResohmCCS811 = db.Column(db.Integer, nullable=False)
    CO2iAQ = db.Column(db.Integer, nullable=False)
    TVOCiAQ = db.Column(db.Integer, nullable=False)
    RiAQCore = db.Column(db.Integer, nullable=False)
    AireMuestra = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Sample('{self.id}', '{self.Sample}', '{self.TempBME680}'," \
               f"'{self.PresureBME680}','{self.HRBME680}', '{self.RBME680}', '{self.CO2SGP30}', '{self.TVOCSGP30}', " \
               f"'{self.H2SGP30}', '{self.EtanolSGP30}','{self.CO2CCS811}', '{self.TVOCCCS811}', '{self.ResohmCCS811}', '{self.CO2iAQ}'," \
               f" '{self.TVOCiAQ}', '{self.RiAQCore}','{self.AireMuestra}')"

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
    type = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    notes = db.Column(db.String(256), nullable=True)
    start_sample_id = db.Column(db.Integer, nullable=True)
    end_sample_id = db.Column(db.Integer, nullable=True)
    filename = db.Column(db.String(256), nullable=True)
    s3_path = db.Column(db.String(256), nullable=False)
    no_of_record = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    additional_docs = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f"Sample('{self.id}', '{self.user_id}', '{self.device_name}'," \
               f"'{self.sample_set_id}','{self.start_sample_id}', '{self.end_sample_id}', '{self.filename}'" \
               f", '{self.s3_path}', '{self.no_of_record}', '{self.date_created}')"


class Samples_userdevices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    device_name = db.Column(db.String(256), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Sample('{self.id}', '{self.user_id}', '{self.device_name}'," \
               f"'{self.date_created}')"
