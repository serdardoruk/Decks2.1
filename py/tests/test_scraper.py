"""
import unittest
import random
import json
from flask_testing import TestCase
from models.database import db
from app import create_app
from models.user import User, CollectionCard
from models.deck import Event, Deck, DeckCard
from models.card import Card
from scraper.xls_parser import XlsParser

class ScraperTest(unittest.TestCase):

	def create_app(self):
		app = create_app(env = "DEV")
		db.init_app(app)
		return app

	def setUp(self):
		db.create_all()
		# load all the cards 
		with open("./data/AllCards.json", "r") as f:
			card_data = json.load(f)
			for name in card_data:
				new_card = Card(name)
				db.session.add(new_card)
			db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_parser(self):
		deck_id = "317074"
		parser = XlsParser()
		this_deck = parser.parse_deck(deck_id)
		self.assertIsNotNone(this_deck)
		query_this_deck = Deck.query.filter_by(deck_id = int(deck_id)).first()
		event = this_deck.event
		self.assertIsNotNone(query_this_deck)
		self.assertIsNotNone(this_deck.event)

		self.assertEqual(this_deck.url, "http://www.mtgtop8.com/event?e=18732&d=317074&f=MO")
		self.assertEqual(event.event_format.replace(" ", ""), "Modern")
		self.assertEqual(event.name, "Modern [Pro Series] @ Fire & Dice")
		self.assertEqual(event.num_players, 32)
		self.assertEqual(event.date.replace(" ", ""), "11/03/18\\n\\t")
		self.assertEqual(this_deck.event_id, 18732)
		self.assertEqual(this_deck.event_placing, "#3-4")
		self.assertEqual(this_deck.name, "BantKnightfall-")
		self.assertEqual(this_deck.player, "Shaunt Azadian")
		self.assertEqual(this_deck.archetype, "Bant")


"""