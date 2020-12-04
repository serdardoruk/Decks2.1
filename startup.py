import os
import time
from app import app
from flask import Flask, render_template, send_from_directory, request, json
from py.routes.api import api
from py.scraper.xls_parser import XlsParser
from py.scraper.mtgtop8_scraper import Mtgtop8_Scraper
from py.models.deck import Deck,DeckCard,Event
from py.models.card import Card
from py.models.database import db 

def create_database():
	with app.app_context():
		db.drop_all()
		db.create_all()
		i = 1
		with open("./py/data/AllCards.json", "r") as f:
			card_data = json.load(f)
			
			for name in card_data:
				# if i > 25:
				# 	break
				info = card_data[name]
				search_card = Card.search_card_by_name(name)
				is_modern_legal = False
				legal_formats = info.get('legalities')
				if legal_formats:
					for f in legal_formats:
						if f.get('format') == "Modern" and f.get('legality') == "Legal":
							is_modern_legal = True
				if search_card is None and is_modern_legal:
					print(name)
					new_card = Card(name)
					db.session.add(new_card)
					i += 1
		db.session.commit()
		# put in the worker to refresh the mtgo scraper 
		scraper = Mtgtop8_Scraper()
		xls_parser = XlsParser()
		starttime = time.time()
		print("tick")
		# wipe deck data here
		# remember you need to delete the decks from the database and 
		# also clear the entire './data/deck_data' directory
		
		# db.session.query(Deck).delete()
		# db.session.query(DeckCard).delete()
		# db.session.query(Event).delete()
		xls_parser.clear_deck_xls_files()

		# save the new decks with scraper 
		print('save')
		os.mkdir('./py/data/deck_data')
		print('made dir')
		scraper.save_modern_decks_fast()
		print('load')
		xls_parser.load_decks_to_db()
		print('done')
		# delay REFRESH_TIME see variable above
		#time.sleep(REFRESH_TIME - ((time.time() - starttime) % REFRESH_TIME))

if __name__ == '__main__':
	create_database()