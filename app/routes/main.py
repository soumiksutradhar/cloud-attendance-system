from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "<h1>Welcome to the Attendance System!</h1>"
