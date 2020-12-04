import os
import time
from flask import Flask, render_template, send_from_directory, request, json
from py.routes.api import api
from py.scraper.xls_parser import XlsParser
from py.scraper.mtgtop8_scraper import Mtgtop8_Scraper
from py.models.deck import Deck,DeckCard,Event
from py.models.card import Card
from py.models.database import db 


def create_app(env = "TEST"):
	TEMPLATE_DIR = os.path.abspath('./py/templates')
	STATIC_DIR = os.path.abspath('./py/static')

	app = Flask(__name__, static_folder = STATIC_DIR, template_folder = TEMPLATE_DIR)	

	# use this if in development mode, will add functionality to adjust 
	# between prod and dev configurations soon
	if env == "TEST":
		app.config.from_object('config.TestingConfig')
	elif env == "DEV":
		app.config.from_object('config.DevelopmentConfig')
	else:
		app.config.from_object('config.DevelopmentConfig')
	return app


DATABASE_URI = os.environ.get('DATABASE_URI')
if DATABASE_URI is None:
	ENV = "TEST"
else:
	ENV = "DEV"

app = create_app(env = ENV)
os.environ['SECRET_KEY'] = app.config['SECRET_KEY']
db.init_app(app) 
app.register_blueprint(api, url_prefix='/api')

@app.after_request
def add_header(response):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame,
	and also to cache the rendered page for 10 minutes.
	"""
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	# for now we cache nothing, this will only be used in development
	response.headers['Cache-Control'] = 'public,max-age=0'
	response.headers['Vary'] = 'Accept-Encoding'
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add("Access-Control-Allow-Credentials", "true")
	response.headers.add("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT")
	response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")
	return response


# @app.errorhandler(404)
# def page_not_found(error):
# 	"""
# 	: Returns an error page, leaving option to report this error somehow later
# 	"""
# 	return render_template("error_page.html")


@app.errorhandler(405)
def method_not_allowed(error):
	"""
	: Will handle method not allowed errors
	"""
	return "No Thanks"

@app.errorhandler(500)
def internal_server_error(error):
	"""
	: Will handle internal server errors and report them to us
	"""
	return "No Thanks"


@app.route('/static/<path:path>', methods = ['GET'])
def send_static(path):
	"""
	: This route allows static files to be retrieved from the server
	"""
	return send_from_directory('static', path)


@app.route('/',defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	"""
	: This route prevents all non-static files from being called by the server
	: apart from index.html
	"""
	return render_template("index.html")