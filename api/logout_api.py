from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
from flask import Flask, session, jsonify
from flask.ext.session import Session
import hashlib
import uuid
import re

logout_api = Blueprint('logout_api', __name__, template_folder='templates')

@logout_api.route("/api/v1/logout", methods = ['GET', 'POST', 'PUT'])
def logoutApi():
	if request.method == "POST" :
		if 'username' in session:
			session.pop('username', None)
			userDict = {
				
			}

			return jsonify(userDict), 204

		else:
			errorDict = {
				"errors": [
					{
						"message": "You do not have the necessary credentials for the resource"
					}
				]
				
			}

			return jsonify(errorDict),401
