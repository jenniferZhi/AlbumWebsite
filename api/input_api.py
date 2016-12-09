from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
from flask import Flask, session, jsonify
from flask.ext.session import Session
import hashlib
import uuid
import re
import datetime, calendar



input_api = Blueprint("input_api", __name__,template_folder='templates')

db = connect_to_database()

@input_api.route("/api/v1/input/<albumid>", methods = ['GET', 'POST', 'PUT'])
def inputApi(albumid):
	if request.method == "GET" :


		cur = db.cursor()
		cur.execute("SELECT * FROM Album WHERE albumid ='"+albumid+"'")
		results_album = cur.fetchall()

		access = results_album[0]['access']
		created = results_album[0]['created']
		lastupdated = results_album[0]['lastupdated']
		results_username = results_album[0]['username']
		title = results_album[0]['title']

		if 'username' in session:

			username = session['username']

			if(username != results_username):

				errorDict = {
					"errors": [
					{
						"message": "You do not have the necessary permissions for the resource"
					}]
				
				} 

				return jsonify(errorDict),403 

			else:
				albumDict = {
					"flag" : "success"
				}

				return jsonify(albumDict)

		else:
			errorDict = {
				"errors": [
				{
					"message": "You do not have the necessary permissions for the resource"
				}]
				
			} 

			return jsonify(errorDict),403 













