from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
import hashlib
import uuid
from flask import Flask, session,jsonify
from flask.ext.session import Session


login = Blueprint('login', __name__, template_folder='templates')

@login.route('/login', methods = ['GET', 'POST'])
def login_route():


	if "username" in session:
		return redirect(url_for('user.user_edit_route()'))


	
	else:
		
		return render_template("login.html") 
