from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
from flask import Flask, session,jsonify
from flask.ext.session import Session

pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods = ['GET', 'POST', 'PUT'])
def pic_route():
	
	return render_template('album_pic.html')

	


