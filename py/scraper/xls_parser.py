import os
import glob
from py.models.deck import Deck,DeckCard, Event
from py.models.card import Card
import shutil 
from py.models.database import db
import xlrd

deck_dir = './py/data/deck_data'


class XlsParser:

	def load_all_decks(self):
		"""
		: loads all decks from './data/deck_data' folder
		"""
		deck_file_names = os.listdir(deck_dir)
		for file_name in deck_file_names:
			deck_id = file_name.split(".")[0]
			self.parse_deck(deck_id)



	def clear_deck_xls_files(self):
		if os.path.isdir(deck_dir):
			shutil.rmtree(deck_dir, ignore_errors=False, onerror=None)

	def parse_deck(self, deck_id):
		"""
		: Parses the deck data directory and returns an object with the card
		: quantities in the collection. 
		: Currently returns a list of tuples, but in the future will return
		: a Deck object defined in decks.py
		"""
		file_name = deck_dir + "/" + deck_id
		print(file_name)
		# if the file doesn't exist then we return None
		if not os.path.isfile(file_name):
			return None

		workbook = xlrd.open_workbook(file_name)
		worksheet = workbook.sheet_by_index(0)

		url = worksheet.cell(0, 1).value
		event_format = worksheet.cell(1,1).value
		event_name = worksheet.cell(2,1).value
		try:
			num_players = int(worksheet.cell(3,1).value.split(" ")[0])
		except:
			num_players = 0
		event_date = worksheet.cell(4,1).value
		deck_id = int(worksheet.cell(5, 1).value)
		event_id = int(worksheet.cell(6,1).value)
		event_placing = worksheet.cell(7,1).value
		deck_name = worksheet.cell(8, 1).value
		player = worksheet.cell(9,1).value
		archetype = worksheet.cell(10,1).value
	
		main_deck = []
		sideboard = []
		for row in range(12, worksheet.nrows):
			quantity = int(worksheet.cell(row, 0).value)
			card_name = worksheet.cell(row , 1).value
			in_main_deck = worksheet.cell(row , 2).value
			new_card = {"name" : card_name, "quantity" : quantity}
			if in_main_deck == 1:
				main_deck.append(new_card)
			else:
				sideboard.append(new_card)
			

		event = Event.query.filter_by(event_id = event_id).first()
		if event is None:
			event = Event.create_event(
				event_id = event_id,
				event_format = event_format,
				name = event_name,
				date = event_date,
				num_players = num_players
			)
		
		new_deck = Deck.create_deck(
			url = url,
			deck_id = deck_id, 
			name = deck_name,
			event = event, 
			event_placing = event_placing, main_deck = main_deck,
			sideboard = sideboard, player = player, archetype = archetype
		)
		
		return new_deck

	def load_decks_to_db(self, limit = float('inf')):
		deck_ids = [f for f in os.listdir(deck_dir) if os.path.isfile(os.path.join(deck_dir, f))]
		print(deck_ids)
		i = 0
		for deck_id in deck_ids:
			print(i)
			self.parse_deck(deck_id)
			i += 1
			if i > limit:
				break




