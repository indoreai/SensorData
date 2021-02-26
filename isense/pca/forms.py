import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed


class UploadForm(FlaskForm):
    device_name = StringField('Device Name', validators=[DataRequired()])
    sample_set_id = StringField('Sample Set', validators=[DataRequired()])
    name = StringField('Name')
    # sample_date = StringField('Sample Date', validators=[DataRequired()])
    type = StringField('Type')
    address = TextAreaField('Address')
    notes = TextAreaField('Notes')
    file = FileField('Upload Sample File', validators=[DataRequired(), FileAllowed(['csv', 'txt'])])
    support_file = FileField('Upload Supported Document')
    submit = SubmitField('Upload')

    def validate_device_name(self, device_name):
        if not re.match("^[A-Za-z0-9_-]*$", device_name.data):
            raise ValidationError('Device Name must contain only letters numbers or underscore')

    def validate_sample_set_id(self, sample_set_id):
        if not re.match("^[A-Za-z0-9_-]*$", sample_set_id.data):
            raise ValidationError('Sample Set must contain only letters numbers or underscore')


class Update_dashboard(FlaskForm):
    device_name = StringField('Device Name')
    sample_set_id = StringField('Sample Set')
    name = StringField('Name')
    # sample_date = StringField('Sample Date', validators=[DataRequired()])
    type = StringField('Type')
    address = TextAreaField('Address')
    notes = TextAreaField('Notes')
    file = FileField('Upload Supported Doc')
    submit = SubmitField('Save')

