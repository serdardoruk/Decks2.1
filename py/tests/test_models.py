import unittest
import random
import json
from flask_testing import TestCase
from models.database import db
from app import create_app
from models.user import User, CollectionCard
from models.deck import Event, Deck, DeckCard
from models.card import Card

LAME_USERNAME = "LAME_USERNAME"
PASSWORD = "PASSWORD"
WRONG_PASSWORD = "WRONG_PASSWORD"
COOL_USERNAME = "COOL_USERNAME"

class ModelTests(TestCase):
	
	def create_app(self):
		app = create_app(env = "TEST")
		db.init_app(app)
		return app
	
	def setUp(self):
		db.create_all()

		# initialize 100 cards 
		for x in range(0, 100):
			new_card = Card("card" + str(x))
			db.session.add(new_card)
		db.session.commit()


	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def generate_event(self):
		new_event = Event(
			event_id = 1234,
			event_format = "Modern", name = "SCG MSP", 
		 	date = db.func.current_timestamp(), num_players = 1000
		)
		db.session.add(new_event)
		db.session.commit()
		return new_event

	def generate_deck(self, n, m):
		event = self.generate_event()
		main_deck_input = []
		for x in range(0, n):
			main_deck_input.append({"name" : "card" + str(x), "quantity" : x  + 1})
		sideboard_input = []
		for x in range(0, m):
			sideboard_input.append({"name" : "card" + str(x), "quantity" : x + 1 })
		new_deck = Deck.create_deck(
			deck_id = 567, 
			name = "test" + str(x), 
			event_placing = x, 
			event = event, 
			main_deck = main_deck_input,
			sideboard = sideboard_input
		)
		return new_deck

	def generate_user(self, username, password):
		user = User(username = username, password = password)
		db.session.add(user)
		db.session.commit()
		return user

	def test_format_string(self):
		pass

	def test_query_cards(self):
		# initialize some sample cards
		# testing comment 
		user = self.generate_user(COOL_USERNAME, PASSWORD)
		card_names = [
			"Jace, The Mind Sculptor",
			"Jace's Defeat",
			"Jace, Vrynn's Prodigy",
			"Jackal Pup",
			"Scalding Tarn",
			"Ancestral Vision",
			"Serum Visions",
			"Lightning Bolt",
			"Forked Bolt",
			"Boltwing Marauder",
			"Firebolt"
		]
		for name in card_names:
			new_card = Card(name)
			db.session.add(new_card)
		db.session.commit()

		# assert that each query for a specific card has exactly one match. 
		# Note for our input that none of the names are substrings of another
		for name in card_names:
			sample = Card.query.filter_by(search_name = Card.format_card_name_for_search(name)).first()
			query = user.query_cards(name)
			self.assertEqual(len(query), 1)

		# these queries have the query amount and expected output
		test_queries = [
			("Tarn", 1),
			("Jace", 3),
			("jace", 3),
			("Jac", 4),
			("bolt", 4),
			("vision", 2),
			("visions", 1)
		]

		for test in test_queries:
			card_name = test[0]
			expected_quantity = test[1]
			query = user.query_cards(card_name)
			self.assertEqual(len(query), expected_quantity)


	def test_card_search_name(self):
		# there's 18000 in this AllCards.json so we only check some of them
		# This variable can be adjusted to check all of them
		# To check all 18000 cards, it will take at least 30 seconds
		# and will bog down other tests
		
		NUM_CARDS_TO_CHECK = 100

		with open("./data/AllCards.json", "r") as f:
			card_data = json.load(f)
			count = 0 
			for name in card_data:
				if count < NUM_CARDS_TO_CHECK:
					new_card = Card(name)
					db.session.add(new_card)
					count += 1
			db.session.commit()

		count = 0
		for name in card_data:
			if count < NUM_CARDS_TO_CHECK:
				card = Card.search_card_by_name(name)
				self.assertIsNotNone(card)
				formatted_name = Card.format_card_name_for_search(name)
				cards = Card.query.filter_by(search_name = formatted_name).all()
				self.assertEqual(len(cards), 1)
				count += 1

	def test_add_user(self):
		no_user = User.query.filter_by(username = COOL_USERNAME).all()
		self.assertEqual(len(no_user), 0)
		user = self.generate_user(COOL_USERNAME, PASSWORD)
		one_user = User.query.filter_by(username = COOL_USERNAME).all()
		self.assertEqual(len(one_user), 1)
		no_user = User.query.filter_by(username = LAME_USERNAME).all()
		self.assertEqual(len(no_user), 0)

	def test_user_jwt(self):
		user_1 = self.generate_user(COOL_USERNAME, PASSWORD)
		jwt = user_1.create_jwt()
		self.assertIsNotNone(jwt)
		jwt_user = User.decode_jwt(jwt)
		self.assertEqual(jwt_user, user_1)
		self.assertEqual(jwt_user.username, user_1.username)
		self.assertEqual(jwt_user.user_id, user_1.user_id)
		null_string = None
		decoded_jwt = User.decode_jwt(null_string)
		self.assertIsNone(decoded_jwt)
		random_string = "qwertyuuiopasdf"
		decoded_jwt = User.decode_jwt(random_string)
		self.assertIsNone(decoded_jwt)

	def test_login_user(self):
		login_user = User.login(COOL_USERNAME, PASSWORD)
		self.assertIsNone(login_user)
		user_1 = self.generate_user(COOL_USERNAME, PASSWORD)
		self.assertIsNone(User.login(LAME_USERNAME, PASSWORD))
		self.assertIsNone(User.login(COOL_USERNAME, WRONG_PASSWORD))
		self.assertIsNone(User.login(None, PASSWORD))
		self.assertIsNone(User.login(COOL_USERNAME, None))
		self.assertIsNone(User.login(None, None))
		login_user = User.login(COOL_USERNAME, PASSWORD)
		self.assertIsNotNone(login_user)
		self.assertEqual(login_user.user_id, user_1.user_id)

	def test_add_card_to_collection(self):
		user = self.generate_user(COOL_USERNAME, PASSWORD)
		# assert the collection starts at size 0
		self.assertEqual(user.collection_size(), 0)

		# assert that adding a card with no quantity doesn't
		# update the size of the collection
		card = Card.query.filter_by(name = "card0").first()
		user.add_card_to_collection(card, 0)
		self.assertEqual(user.collection_size(), 0)

		# add cards with random non-negative quantities
		# and assert the new size of the collection
		running_size = 0
		for x in range(0, 100):
			quantity = random.randint(0,20)
			# we divide by 2 so we add the same card multiple times
			name = "card" + str(x // 3) 
			card = Card.query.filter_by(name = name).first()
			user.add_card_to_collection(card, quantity)
			running_size += quantity
			self.assertEqual(user.collection_size(), running_size)


	def test_remove_card_from_collection(self):
		user = self.generate_user(COOL_USERNAME, PASSWORD)
		# assert the collection starts at size 0
		self.assertEqual(user.collection_size(), 0)

		#assert that trying to remove a card from an empty collection
		#that nothing happens
		for x in range(0,100):
			quantity = random.randint(0,10) - 10
			name = "card" + str(x // 3)
			card = Card.query.filter_by(name = name).one()
			user.remove_card_from_collection(card, quantity)
			self.assertEqual(user.collection_size(), 0)

		#populate the collection and keep track of size
		running_size = 0
		for x in range(0, 100):
			quantity = random.randint(0,20)
			# we divide by 2 so we add the same card multiple times
			name = "card" + str(x // 3) 
			card = Card.query.filter_by(name = name).first()
			user.add_card_to_collection(card, quantity)
			running_size += quantity
			self.assertEqual(user.collection_size(), running_size)

		# remove cards with random quantities - including negative
		# if quantity is <= 0 running size should stay the same
		# if quantity is > collection[cardname] running size should stay the same
		# else decrement running size by quantity
		for x in range(0,100):
			quantity = random.randint(0,50)
			name = "card" + str(x // 3)
			card = Card.query.filter_by(name = name).one()
			existing_card = CollectionCard.query.filter_by(user_id = user.user_id, card_id = card.card_id).first()
			if existing_card:
				existing_quantity = existing_card.quantity	
			else:
				existing_quantity = 0
				# we've changed this method so that if we remove all copies of the card from the collection
				# if we try to remove more than we have
			running_size -= min(quantity, existing_quantity)
			user.remove_card_from_collection(card, quantity)
			self.assertEqual(user.collection_size(), running_size)

	def test_missing_card_from_main_deck(self):
		user = self.generate_user(COOL_USERNAME, PASSWORD)
		self.assertEqual(user.collection_size(), 0)
		test_main_deck = []
		empty_sideboard =[]
		UNIQUE_CARDS_IN_MAIN_DECK = 20
		UNIQUE_CARDS_IN_SIDEBOARD = 10
		test_deck = self.generate_deck(UNIQUE_CARDS_IN_MAIN_DECK, UNIQUE_CARDS_IN_SIDEBOARD)

		#an empty collection should be missing every card from a maindeck
		cards_missing_from_main_deck = user.missing_cards_from_main_deck(test_deck)
		
		#assert that the number of unique cards missing are the same
		self.assertEqual(len(cards_missing_from_main_deck), UNIQUE_CARDS_IN_MAIN_DECK)

		# assert that the quantities of each card are also equal
		for card in cards_missing_from_main_deck:
			name = card['name']
			quantity = card['quantity']
			deck_card = DeckCard.query.filter_by(card_id = card['card'].card_id, deck_id = test_deck.deck_id, is_main_deck = True).first()
			self.assertEqual(name, deck_card.card.name)
			self.assertEqual(quantity, deck_card.quantity)

		#a "full" collection should be missing no card from a maindeck
		for x in range(0,UNIQUE_CARDS_IN_MAIN_DECK):
			quantity = 100
			name  = "card" + str(x)
			card = Card.query.filter_by(name = name).one()
			user.add_card_to_collection(card, quantity)

		cards_missing_from_main_deck = user.missing_cards_from_main_deck(test_deck)
		self.assertEqual(len(cards_missing_from_main_deck),0)

		# now we remove cards to create a 'partially full' collection.
		# a "partially full" collection should be missing some cards from a maindeck
		user_2 = self.generate_user(LAME_USERNAME, PASSWORD)
		self.assertEqual(user_2.collection_size(), 0)
		
		# we add half the cards to the collection in random quantities
		for x in range(0,UNIQUE_CARDS_IN_MAIN_DECK // 2):
			quantity = random.randint(0, 2)
			name = "card" + str(x)
			card = Card.query.filter_by(name = name).one()
			user_2.add_card_to_collection(card, quantity)
		cards_missing_from_main_deck = user_2.missing_cards_from_main_deck(test_deck)

		# here we compute what the missing cards output should look like
		missing_dict = {}
		for card in test_deck.main_deck:
			collection_card = CollectionCard.query.filter_by(card_id = card.card.card_id, user_id = user_2.user_id).first()
			if not collection_card:
				missing_dict[card.card.name] = card.quantity				
			elif collection_card.quantity < card.quantity:
				missing_dict[card.card.name] = card.quantity - collection_card.quantity

		# verify that missing cards matches up
		for card in cards_missing_from_main_deck:
			self.assertIsNotNone(missing_dict.get(card['card'].name))
			self.assertEqual(card.get('quantity'), missing_dict.get(card['card'].name))
	

	def test_missing_cards_from_deck(self):
		user = self.generate_user(COOL_USERNAME, PASSWORD)
		self.assertEqual(user.collection_size(), 0)
		test_main_deck = []
		empty_sideboard =[]
		UNIQUE_CARDS_IN_MAIN_DECK = 2
		UNIQUE_CARDS_IN_SIDEBOARD = 4
		test_deck = self.generate_deck(UNIQUE_CARDS_IN_MAIN_DECK, UNIQUE_CARDS_IN_SIDEBOARD)
		#an empty collection should be missing every card from a maindeck
		missing_cards = user.missing_cards_from_deck(test_deck)
		
		#assert that the number of unique cards missing are the same
		self.assertEqual(len(missing_cards), max(UNIQUE_CARDS_IN_MAIN_DECK, UNIQUE_CARDS_IN_SIDEBOARD))

		# assert that the quantities of each card are also equal for an empty collection
		for card in missing_cards:
			name = card['name']
			quantity = card['quantity']
			card = card['card']
			deck_cards = DeckCard.query.filter_by(card_id = card.card_id, deck_id = test_deck.deck_id).all()
			expected_quantity = 0
			for x in deck_cards:
				expected_quantity += x.quantity
			self.assertEqual(name, deck_cards[0].card.name)
			self.assertEqual(quantity, expected_quantity)

		# we add 3 of each card to the collection
		for x in range(0, 7):
			quantity = 2
			name = "card" + str(x)
			card = Card.query.filter_by(name = name).one()
			user.add_card_to_collection(card, quantity)

		missing_cards = user.missing_cards_from_deck(test_deck)
		for card in missing_cards:
			if card['name'] == 'card1':
				self.assertEqual(card['quantity'], 2)
			elif card['name'] == 'card2':
				self.assertEqual(card['quantity'], 1)
			elif card['name'] == 'card3':
				self.assertEqual(card['quantity'], 2)	
			

		# add to the rest of the collection
		for x in range(0, 7):
			quantity = 2
			name = "card" + str(x)
			card = Card.query.filter_by(name = name).one()
			user.add_card_to_collection(card, quantity)

		missing_cards = user.missing_cards_from_deck(test_deck)
		self.assertEqual(len(missing_cards),0)


