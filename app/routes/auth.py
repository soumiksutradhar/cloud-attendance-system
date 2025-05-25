from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
	return "<h2>Login Page</h2>"

# Registers and logout routes to be added later here
