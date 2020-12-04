import os
import time
from app import app
from py.models.database import db 
from py.scraper.mtgtop8_scraper import Mtgtop8_Scraper
from py.models.card import Card
from py.scraper.xls_parser import XlsParser
from py.models.deck import Deck,DeckCard,Event
from flask import Flask, render_template, send_from_directory, request, json




def refresh_decks_function():
	# also initialize a set of decks now
	# We should call this method so that it refreshes the decks once a week or something
	# We add all cards from AllCards.json to the databse
	with app.app_context():
		# put in the worker to refresh the mtgo scraper 
		xls_parser = XlsParser()
		xls_parser.clear_deck_xls_files()
		os.mkdir('./py/data/deck_data')
		scraper = Mtgtop8_Scraper()
		
		starttime = time.time()
		print("tick")
		# wipe deck data here
		# remember you need to delete the decks from the database and 
		# also clear the entire './data/deck_data' directory
		

		# this query is a cascade delete too
		decks = Deck.query.all()
		for deck in decks:
			db.session.delete(deck)
		db.session.commit()
		
		# save the new decks with scraper 
		print('save')

		
		scraper.save_modern_decks_fast()
		print('load')
		xls_parser.load_decks_to_db()
		# delay REFRESH_TIME see variable above
		#time.sleep(REFRESH_TIME - ((time.time() - starttime) % REFRESH_TIME))


if __name__ == "__main__":
	refresh_decks_function()