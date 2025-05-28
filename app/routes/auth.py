from datetime import datetime, date
import pytz
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.user import User
from app import db
from app.forms.auth_forms import RegistrationForm, LoginForm
from app.decorators import roles_required
from app.models.attendance import Attendance, AttendanceWindow
from app.forms import AttendanceWindowForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        # Create new user
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.data.role.lower()  # Sets role for user
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    IST = pytz.timezone('Asia/Kolkata')
    print("Form fields:", form._fields)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome back, {user.username}!", 'success')

            if user.role == 'student':
                today = datetime.now(IST).date()
                now = datetime.now(IST).time()

                window = AttendanceWindow.query.filter_by(date=today).first()
                if window:
                    if window.start_time <= now <= window.end_time:
                        already_marked = Attendance.query.filter_by(student_id=user.id, date=today).first()
                        if not already_marked:
                            new_attendance = Attendance(student_id=user.id, date=today, time_marked=now, status='Present')
                            db.session.add(new_attendance)
                            db.session.commit()
                            flash('✅ Your attendance has been marked successfully.', 'success')
                        else:
                            flash('⚠️ Attendance already marked for today.', 'info')
                    else:
                        flash('⚠️ You logged in outside the attendance window.', 'warning')
                else:
                    flash('⚠️ Attendance window not set for today.', 'warning')


            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@auth.route('/teacher-dashboard')
@login_required
@roles_required('teacher', 'admin')  # Only teachers and admins can access
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

@auth.route('/set-attendance-window', methods=['GET', 'POST'])
@login_required
@roles_required('teacher', 'admin')
def set_attendance_window():
    form = AttendanceWindowForm()

    # Check if window already exists for today
    today = date.today()
    window = AttendanceWindow.query.filter_by(date=today).first()

    if form.validate_on_submit():
        start = form.start_time.data
        end = form.end_time.data

        if start >= end:
            form.end_time.errors.append('End time must be after start time.')
            return render_template('set_attendance_window.html', form=form, window=window)

        if window:
            # Update existing window
            window.start_time = start
            window.end_time = end
            window.created_by = current_user.id
        else:
            # Create new window
            window = AttendanceWindow(
                date=today,
                start_time=start,
                end_time=end,
                created_by=current_user.id
            )
            db.session.add(window)

        db.session.commit()
        flash('Attendance window set successfully!', 'success')
        return redirect(url_for('auth.teacher_dashboard'))

    # Pre-fill form if window exists
    if window and request.method == 'GET':
        form.start_time.data = window.start_time
        form.end_time.data = window.end_time

    return render_template('set_attendance_window.html', form=form, window=window)
