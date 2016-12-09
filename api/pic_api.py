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

pic_api = Blueprint("pic_api", __name__,template_folder='templates')

db = connect_to_database()

@pic_api.route("/api/v1/pic/<picid>", methods = ['GET', 'POST', 'PUT'])
def picidApi(picid):
	if request.method == "GET" :

		cur = db.cursor()
		cur.execute("SELECT * FROM Photo WHERE picid='%s'" %picid)
		results_photo = cur.fetchall()
		cur.execute("SELECT * FROM Contain WHERE picid='%s'" %picid)
		results_contain = cur.fetchall()
		if results_photo == ():

			errorDict = {
				"errors": [
					{
						"message": "The requested resource could not be found"
					}
				]
				
			} 

			return jsonify(errorDict),404

		format = results_photo[0]['format']
		date = results_photo[0]['date']
		albumid = results_contain[0]['albumid']
		caption = results_contain[0]['caption']
		sequencenum = results_contain[0]['sequencenum']

		print "original sequencenum"
		print sequencenum

		cur1 = db.cursor()
		cur1.execute('SELECT max(sequencenum) FROM Contain WHERE sequencenum < %s AND albumid = %s', (sequencenum, albumid))
		preseq = cur1.fetchall()[0]['max(sequencenum)']

		if preseq == None:
			preseq = sequencenum

		cur2 = db.cursor()
		cur2.execute('SELECT min(sequencenum) FROM Contain WHERE sequencenum > %s AND albumid = %s', (sequencenum, albumid))
		nextseq = cur2.fetchall()[0]['min(sequencenum)']


		if nextseq == None:
			print "orange"
			nextseq = sequencenum

		cur3 = db.cursor()
		cur3.execute('SELECT picid FROM Contain WHERE sequencenum = %s', (preseq, ))
		prev = cur3.fetchall()[0]['picid']


		cur4 = db.cursor()
		cur4.execute('SELECT picid FROM Contain WHERE sequencenum = %s', (nextseq, ))
		next = cur4.fetchall()[0]['picid']

		cur5 = db.cursor()
		cur5.execute('SELECT * FROM Album WHERE albumid = %s', (albumid, ))
		results_album = cur5.fetchall()

		results_username = results_album[0]['username']
		access = results_album[0]['access']

		if 'username' in session:

			username = session['username']

			if(username != results_username and access == 'private'):

				cur6 = db.cursor()
				cur6.execute("SELECT username FROM AlbumAccess WHERE albumid='%s'" %albumid)
				results_search_username = cur6.fetchall()
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

			picDict = {
							"albumid": albumid,
							"caption": caption,
							"format": format,
							"next": next,
							"picid": picid,
							"prev": prev
			}

			return jsonify(picDict)

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

			picDict = {
							"albumid": albumid,
							"caption": caption,
							"format": format,
							"next": next,
							"picid": picid,
							"prev": prev
			}

			return jsonify(picDict)

	elif request.method == 'PUT':

		if 'username' in session:

			username = session['username']
			picdata = request.get_json()

			if len(picdata) != 6:
				errorDict = {
					"errors": [
						{
							"message": "You did not provide the necessary fields"
						}
					]
					
				}
				return jsonify(errorDict),422

			albumid = picdata['albumid']
			caption = picdata['caption']
			format = picdata['format']
			next = picdata['next']
			picid = picdata['picid']
			prev = picdata['prev']

			cur = db.cursor()
			cur.execute("SELECT * FROM Photo WHERE picid='%s'" %picid)
			results_photo = cur.fetchall()

			if results_photo == ():

				errorDict = {
					"errors": [
						{
							"message": "The requested resource could not be found"
						}
					]
					
				} 

				return jsonify(errorDict),404

			cur1 = db.cursor()
			cur1.execute('SELECT * FROM Album WHERE albumid = %s', (albumid, ))
			results_album = cur1.fetchall()

			results_username = results_album[0]['username']
			access = results_album[0]['access']

			if(username != results_username and access == 'private'):

				cur2 = db.cursor()
				cur2.execute("SELECT username FROM AlbumAccess WHERE albumid='%s'" %albumid)
				results_search_username = cur2.fetchall()
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

			cur3 = db.cursor()
			cur3.execute("SELECT * FROM Photo WHERE picid='%s'" %picid)
			results_photo = cur3.fetchall()

			result_format = results_photo[0]['format']

			if result_format != format:

				errorDict = {
						"errors": [
						{
							"message": "You can only update caption"
						}
					]
				
				} 

				return jsonify(errorDict),403

			cur4 = db.cursor()
			cur4.execute('UPDATE Contain SET caption = %s WHERE picid = %s',(caption,picid,))
			cur4.execute('UPDATE Album SET lastupdated = %s WHERE albumid = %s', (datetime.datetime.now(), albumid))

			picDict = {
							"albumid": albumid,
							"caption": caption,
							"format": format,
							"next": next,
							"picid": picid,
							"prev": prev
			}

			return jsonify(picDict),200


		else:
			errorDict = {
						"errors": [
						{
							"message": "You do not have the necessary credentials for the resource"
						}
					]
				
			} 

			return jsonify(errorDict),401












