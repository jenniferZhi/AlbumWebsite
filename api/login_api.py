from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
from flask import Flask, session, jsonify
from flask.ext.session import Session
import hashlib
import uuid
import re

login_api = Blueprint("login_api", __name__,template_folder='templates')
def passwordCreated(password):
	algorithm = 'sha512'
	salt = uuid.uuid4().hex
	print salt

	m = hashlib.new(algorithm)
	m.update(salt + password)
	password_hash = m.hexdigest()

	return "$".join([algorithm, salt, password_hash])



def passwordCheck(salt, password):
	algorithm = 'sha512'
	m = hashlib.new(algorithm)
	m.update(salt + password)
	password_hash = m.hexdigest()

	return "$".join([algorithm, salt, password_hash])

db = connect_to_database()

@login_api.route("/api/v1/login", methods = ['GET', 'POST', 'PUT'])
def loginApi():
	if request.method == "POST" :
		logindata = request.get_json()
		print logindata
		if len(logindata) != 2:
			errorDict = {
				"errors": [
					{
						"message": "You did not provide the necessary fields"
					}
				]
				
			}
			return jsonify(errorDict),422

		username = logindata['username']
		password = logindata['password']

		cur = db.cursor()
		cur.execute("SELECT password FROM User WHERE username='"+username+"'")
		results_password = cur.fetchall()
		if results_password == ():

			errorDict = {
				"errors": [
					{
						"message": "Username does not exist"
					}
				]
				
			}

			return jsonify(errorDict),404

		else:
			salt = results_password[0]['password'].rsplit('$', 2)[1]
			password = passwordCheck(salt, password)

			if password != results_password[0]['password']:

				errorDict = {
					"errors": [
						{
							"message": "Password is incorrect for the specified username"
						}
					]
			
				}

				return jsonify(errorDict),422

			loginDict = {
				"username": username
			}
			session['username'] = username

			return jsonify(loginDict)









