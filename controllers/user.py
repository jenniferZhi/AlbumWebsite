from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
from flask import Flask, session,jsonify
from flask.ext.session import Session
import hashlib
import uuid
import re


user = Blueprint('user', __name__, template_folder='templates')

@user.route('/user', methods = ['GET', 'POST','PUT'])
def user_route():
	if "username" in session:
		return redirect(url_for('user.user_edit_route()'))
	else:
		return render_template('user.html')

@user.route('/user/edit', methods = ['GET', 'POST', 'PUT'])
def user_edit_route():
	if "username" in session:
		username = session['username']

		db =connect_to_database()
		cur = db.cursor()
		cur.execute("SELECT * FROM User WHERE username = '"+username+"' ")
		result_user = cur.fetchall()

		return render_template("userEdit.html", user = result_user)
	else:
		return redirect(url_for('login.login_route()'))