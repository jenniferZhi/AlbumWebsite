from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
from flask import Flask, session, jsonify
from flask.ext.session import Session
import hashlib
import uuid
import re

album_api = Blueprint("album_api", __name__,template_folder='templates')

db = connect_to_database()

@album_api.route("/api/v1/album/<albumid>", methods = ['GET', 'POST', 'PUT'])
def albumApi(albumid):
	if request.method == "GET" :
		#albumdata = request.get_json()
		#albumdata = request.get_json()



		cur = db.cursor()
		cur.execute("SELECT * FROM Album WHERE albumid ='"+albumid+"'")
		results_album = cur.fetchall()
		if results_album == ():

			errorDict = {
				"errors": [
					{
						"message": "The requested resource could not be found"
					}
				]
				
			} 

			return jsonify(errorDict),404

		access = results_album[0]['access']
		created = results_album[0]['created']
		lastupdated = results_album[0]['lastupdated']
		results_username = results_album[0]['username']
		title = results_album[0]['title']

		if 'username' in session:

			username = session['username']

			if(username != results_username and access == 'private'):

				cur1 = db.cursor()
				cur1.execute("SELECT username FROM AlbumAccess WHERE albumid='%s'" %albumid)
				results_search_username = cur1.fetchall()
				flag = 0
				for item in results_search_username:
					if (item['username'] == username):
						flag = 1
				if flag == 0:

					errorDict = {
						"errors": [
						{
							"message": "You do not have the necessary permissions for the resource"
						}
						]
				
					} 

					return jsonify(errorDict),403 

			albumDict = {
							"access": access,
							"albumid": long(albumid),
							"created": created,
							"lastupdated" : lastupdated,
							"pics":[

							],
							"title":title,
							"username": results_username
			}

			cur2 = db.cursor()
			cur2.execute("SELECT * FROM Contain WHERE albumid = '%s'" %albumid)
			results_contain = cur2.fetchall()

			for contain in results_contain:
				caption = contain['caption']
				sequencenum = contain['sequencenum']
				picid = contain['picid']

				cur3 = db.cursor()
				cur3.execute("SELECT * FROM Photo WHERE picid = '%s'" %picid)
				results_photo = cur3.fetchall()
				date = results_photo[0]['date']
				format = results_photo[0]['format']

				albumDict["pics"].append({"albumid": long(albumid), "caption":caption, "date":date, "format":format, "picid":picid, "sequencenum": sequencenum})

			return jsonify(albumDict)


		else:
			if(access == 'private'):

				errorDict = {
						"errors": [
						{
							"message": "You do not have the necessary credentials for the resource"
						}
					]
				
				} 

				return jsonify(errorDict),401

			albumDict = {
							"access": access,
							"albumid": long(albumid),
							"created": created,
							"lastupdated" : lastupdated,
							"pics":[

							],
							"title":title,
							"username": results_username
			}

			cur4 = db.cursor()
			cur4.execute("SELECT * FROM Contain WHERE albumid = '%s'" %albumid)
			results_contain = cur4.fetchall()

			for contain in results_contain:
				caption = contain['caption']
				sequencenum = contain['sequencenum']
				picid = contain['picid']

				cur5 = db.cursor()
				cur5.execute("SELECT * FROM Photo WHERE picid = '%s'" %picid)
				results_photo = cur5.fetchall()
				date = results_photo[0]['date']
				format = results_photo[0]['format']

				albumDict["pics"].append({"albumid": long(albumid), "caption":caption, "date":date, "format":format, "picid":picid, "sequencenum": sequencenum})

			return jsonify(albumDict)
















