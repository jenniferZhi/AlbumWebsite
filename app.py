from flask import *
import MySQLdb
import MySQLdb.cursors
import controllers
import api
from extensions import *
from werkzeug.utils import secure_filename
import os
import hashlib
from flask import Flask, request, redirect, url_for, flash,jsonify

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder = "templates")

app.secret_key = 'jinxiaoyuzhihaiboshenchangju'

app.register_blueprint(controllers.main, url_prefix='/7dzyltg7/p3')
app.register_blueprint(controllers.user, url_prefix='/7dzyltg7/p3')
app.register_blueprint(controllers.login, url_prefix='/7dzyltg7/p3')
app.register_blueprint(controllers.albums, url_prefix='/7dzyltg7/p3')
app.register_blueprint(controllers.album, url_prefix='/7dzyltg7/p3')
app.register_blueprint(controllers.pic, url_prefix='/7dzyltg7/p3')

app.register_blueprint(api.user_api, url_prefix = '/7dzyltg7/p3')
app.register_blueprint(api.album_api, url_prefix = '/7dzyltg7/p3')
app.register_blueprint(api.login_api, url_prefix = '/7dzyltg7/p3')
app.register_blueprint(api.logout_api, url_prefix = '/7dzyltg7/p3')
app.register_blueprint(api.pic_api, url_prefix = '/7dzyltg7/p3')
app.register_blueprint(api.input_api, url_prefix = '/7dzyltg7/p3')


# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)