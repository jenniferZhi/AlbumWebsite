from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
from flask import Flask, session, jsonify
from flask.ext.session import Session
import hashlib
import uuid
import re

def passwordCreated(password):
	algorithm = 'sha512'
	salt = uuid.uuid4().hex

	m = hashlib.new(algorithm)

	m.update(salt + password)
	password_hash = m.hexdigest()
	return "$".join([algorithm, salt, password_hash])

user_api = Blueprint("user_api", __name__,template_folder='templates')

db = connect_to_database()

@user_api.route("/api/v1/user", methods = ['GET', 'POST', 'PUT'])
def userApi():
	if request.method == "GET" :
		if 'username' in session:
			username = session['username']
			cur = db.cursor()
			cur.execute("SELECT * FROM User WHERE username = '"+username+"' ")
			result_user = cur.fetchall()
			firstname = result_user[0]['firstname']
			lastname = result_user[0]['lastname']
			email = result_user[0]['email']

			userDict = {
				"username": username,
				"firstname": firstname,
				"lastname" : lastname,
				"email" : email
			}

			return jsonify(userDict)

		else:
			errorDict = {
				"errors": [
					{
						"message": "You do not have the necessary credentials for the resource"
					}
				]
				
			}

			return jsonify(errorDict),401


	elif request.method == "POST" :
		userdata = request.get_json()
		print "orange"

		if len(userdata) != 6:
			print len(userdata)
			errorDict = {
				"errors": [
					{
						"message": "You did not provide the necessary fields"
					}
				]
				
			}
			return jsonify(errorDict),422

		username = userdata['username']
		firstname = userdata['firstname']
		lastname = userdata['lastname']
		password1 = userdata['password1']
		password2 = userdata['password2']
		email = userdata['email']


		errorDict = {
				"errors": [
					
				]
				
		}

		cur1 = db.cursor()
		cur1.execute("SELECT * FROM User WHERE username = '"+username+"'")
		result_search = cur1.fetchall()
		if result_search != ():
			errorDict["errors"].append({"message":"This username is taken"})

		if len(username) < 3:
			errorDict["errors"].append({"message":"Usernames must be at least 3 characters long"})

		if not re.match("^[a-zA-Z0-9_]+$", username):
			errorDict["errors"].append({"message":"Usernames may only contain letters, digits, and underscores"})

		if len(password1) < 8:
			errorDict["errors"].append({"message":"Passwords must be at least 8 characters long"})

		if re.match('^[0-9]*$', password1) or re.match('^[a-zA-Z]*$', password1):
			errorDict["errors"].append({"message":"Passwords must contain at least one letter and one number"})

		if not re.match('^[0-9a-zA-Z_]*$', password1):	
			errorDict["errors"].append({"message":"Passwords may only contain letters, digits, and underscores"})

		if password1 != password2:
			errorDict["errors"].append({"message":"Passwords do not match"})

		if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			errorDict["errors"].append({"message":"Email address must be valid"})

		if len(username) > 20:
			errorDict["errors"].append({"message":"Username must be no longer than 20 characters"})

		if len(firstname) > 20:
			errorDict["errors"].append({"message":"Firstname must be no longer than 20 characters"})

		if len(lastname) > 20:
			errorDict["errors"].append({"message":"Lastname must be no longer than 20 characters"})

		if len(email) > 40:
			errorDict["errors"].append({"message":"Email must be no longer than 40 characters"})

		print len(errorDict["errors"])
		print "orange again"
		print errorDict["errors"]
		if len(errorDict["errors"]) != 0:
			return jsonify(errorDict),422

		cur2 = db.cursor()
		password = passwordCreated(password1)
		cur2.execute("INSERT INTO User VALUES ('"+username+"', '"+firstname+"', '"+lastname+"', '"+password+"', '"+email+"')")
		userDict = {
				"username": username,
				"firstname": firstname,
				"lastname" : lastname,
				"email" : email
		}

		return jsonify(userDict), 201



	elif request.method == "PUT" :
		if 'username' in session:
			username = session['username']
			userdata = request.get_json()
			result_username = userdata['username']
			result_username = username
			firstname = userdata['firstname']
			lastname = userdata['lastname']
			password1 = userdata['password1']
			password2 = userdata['password2']
			email = userdata['email']

			if username != result_username:
				errorDict = {
				"errors": [
					{
						"message": "You do not have the necessary permissions for the resource"
					}
					]
				
			  	}

				return jsonify(errorDict),403

			else:
				errorDict = {
					"errors": [
					
					]
				
				}
				

				if password1 != password2:
					errorDict["errors"].append({"message":"Passwords do not match"})

				if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
					errorDict["errors"].append({"message":"Email address must be valid"})

		

				if len(firstname) > 20:
					errorDict["errors"].append({"message":"Firstname must be no longer than 20 characters"})

				if len(lastname) > 20:
					errorDict["errors"].append({"message":"Lastname must be no longer than 20 characters"})

				if len(email) > 40:
					errorDict["errors"].append({"message":"Email must be no longer than 40 characters"})

				if len(errorDict["errors"]) != 0:
					return jsonify(errorDict),422

				cur3 = db.cursor()
				if password1 == "":
					cur3.execute("UPDATE User SET firstname = '"+firstname+"',lastname = '"+lastname+"',email = '"+email+"' WHERE username = '"+username+"'")
				else:
					if len(password1) < 8:
						errorDict["errors"].append({"message":"Passwords must be at least 8 characters long"})
					if re.match('^[0-9]*$', password1) or re.match('^[a-zA-Z]*$', password1):	
						errorDict["errors"].append({"message":"Passwords must contain at least one letter and one number"})
					if not re.match('^[0-9a-zA-Z_]*$', password1):
						errorDict["errors"].append({"message":"Passwords may only contain letters, digits, and underscores"})
						
					if len(errorDict["errors"]) != 0:
						return jsonify(errorDict),422
					password = passwordCreated(password1)
					cur3.execute("UPDATE User SET firstname = '"+firstname+"',lastname = '"+lastname+"',password = '"+password+"',email = '"+email+"' WHERE username = '"+username+"'")

				userDict = {
					"username": username,
					"firstname": firstname,
					"lastname" : lastname,
					"email" : email
				}

				return jsonify(userDict), 201
		


		else:
			errorDict = {
				"errors": [
					{
						"message": "You do not have the necessary credentials for the resource"
					}
				]
				
			}

			return jsonify(errorDict),401






