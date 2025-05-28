from datetime import datetime
from app import db

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    time_marked = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
    status = db.Column(db.String(10), nullable=False, default='Present')

    __table_args__ = (db.UniqueConstraint('student_id', 'date', name='unique_attendance_per_day'),)

class AttendanceWindow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
