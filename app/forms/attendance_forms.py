from flask_wtf import FlaskForm
from wtforms import TimeField, SubmitField
from wtforms.validators import DataRequired

class AttendanceWindowForm(FlaskForm):
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Set Attendance Window')
