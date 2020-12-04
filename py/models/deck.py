
import jwt
import os
from passlib.hash import argon2
from flask_sqlalchemy import SQLAlchemy
from py.models.database import db
from py.models.model_config import TableNames
from py.models.card import Card


class DeckCard(db.Model):
	__tablename__ = TableNames.DeckCard

	deck_card_id = db.Column(db.Integer, primary_key=True, unique = True, autoincrement = True)
	deck_id = db.Column(db.Integer, db.ForeignKey(TableNames.Deck + '.deck_id'), nullable = False)
	card_id = db.Column(db.Integer, db.ForeignKey(TableNames.Card + '.card_id'), nullable = False)
	quantity = db.Column(db.Integer, nullable = False)
	is_main_deck = db.Column(db.Boolean, nullable = False)
	card = db.relationship(TableNames.Card , lazy = True,
		primaryjoin="Card.card_id == DeckCard.card_id")

	date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
										   onupdate=db.func.current_timestamp())


class Event(db.Model):
	__tablename__ = TableNames.Event
	# this event_id is the e argument in 
	# http://www.mtgtop8.com/event?e=19120&d=320734&f=LE
	event_id = db.Column(db.Integer, primary_key=True, unique = True)
	decks = db.relationship(TableNames.Deck, backref = "event", lazy = True,
		primaryjoin="Event.event_id == Deck.event_id", cascade = "all,delete")

	event_format = db.Column(db.String)
	name = db.Column(db.String)
	date = db.Column(db.String)
	num_players = db.Column(db.Integer)
	date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
										   onupdate=db.func.current_timestamp())

	@staticmethod
	def create_event(**kwargs):
		event = Event(**kwargs)
		db.session.add(event)
		db.session.commit()
		return event



class Deck(db.Model):
	__tablename__ = TableNames.Deck
	# this deck id is the d argument in 
	# http://www.mtgtop8.com/event?e=19120&d=320734&f=LE


	deck_id = db.Column(db.Integer, primary_key=True, unique = True)

	main_deck = db.relationship(TableNames.DeckCard, lazy = True, cascade = "all,delete",
		primaryjoin="and_(Deck.deck_id == DeckCard.deck_id, DeckCard.is_main_deck == True)")
	sideboard = db.relationship(TableNames.DeckCard, lazy = True, cascade = "all,delete",
		primaryjoin="and_(Deck.deck_id == DeckCard.deck_id, DeckCard.is_main_deck == False)")

	event_id = db.Column(db.Integer, db.ForeignKey(TableNames.Event + '.event_id'), nullable = False)
	name = db.Column(db.String)
	event_placing = db.Column(db.String)
	player = db.Column(db.String)
	url = db.Column(db.String)
	archetype = db.Column(db.String)

	
	date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
										   onupdate=db.func.current_timestamp())

	def main_deck_size(self):
		"""
		: Returns the number of cards in the main_deck
		: Return type: integer
		"""

	def sideboard_size(self):
		"""
		: We have no limit on number of cards in the sideboard for now
		: Returns the number of cards in the sideboard
		: Return type: integer
		"""

	def missing_cards_from_deck(deck, tmp_collection):
		"""
		: deck : Deck object from deck.py
		: Given a deck returns a tuple with 2 lists of 
		: card objects indicating which cards are missing 
		: from the main deck and sideboard
		: return type: list of tuples with Card object and quantity 
		: example output: [(name, quantity),....]
		"""
		md_list = deck.main_deck
		sb_list = deck.sideboard
		needed_list = {}
		for deck_card in (md_list + sb_list):
			card_id = deck_card.card_id
			if needed_list.get(card_id):
				needed_list[card_id] += deck_card.quantity
			else:
				needed_list[card_id] = deck_card.quantity

		output = []
		for card_id, quantity in needed_list.items():
			#collection_card = CollectionCard.query.filter_by(user_id = self.user_id, card_id = card_id).first()
			in_tmp_collection_flag = 0
			cur_quantity = -1
			for dic in tmp_collection:
				cur_card_id = dic['card_id']
				if cur_card_id == card_id:
					in_tmp_collection_flag = 1
					cur_quantity = dic['quantity']
			
			this_card  = Card.query.filter_by(card_id = card_id).first()
			if in_tmp_collection_flag:
				if cur_quantity < quantity:
					card_dict = {"card_id": this_card.card_id, "quantity": quantity - cur_quantity, "card": this_card.serialize()}
					output.append(card_dict)
			else:
				card_dict = {"card_id": this_card.card_id, "quantity": quantity, "card": this_card.serialize()}
				output.append(card_dict)

		return output

	def has_deck(deck, tmp_collection, missing_cards = 0):
		"""
		: deck : Deck object from deck.py
		: given a deck returns True if this collection can make the given deck 
 		: with this collection. 
 		: Optinal missing_cards parameter allows that many number of 
 		: cards from the collection that cannot be in the deck.
 		: 
 		: Example: if a user had all of Jeskai except 4 Scalding Tarns
 		: this function would return True for arguemnts (Jeskai, misisng_cards) where
 		: missing_cards >= 4 and false for missing_cards < 4

 		: return type: boolean
		"""
		if deck is None:
			return None
		missing_from_whole_deck = Deck.missing_cards_from_deck(deck,tmp_collection)
		if (missing_from_whole_deck is None) and missing_cards == 0:
			return True
		count = 0
		for triple in missing_from_whole_deck:
			count += triple["quantity"]
		has_deck_flag = (count <= missing_cards)
		return (has_deck_flag,missing_from_whole_deck)

	@staticmethod
	def remove_deck_from_tmp(deck, tmp_collection):
		"""
		: for every card in the deck, remove each card and it's quantity
		: from the collection. If the collection doesn't have every card in the deck
		: then do nothing to the collection and return None. Otherwise return the deck object
		: return type: deck object
		"""
		#{'card': {'card_id': 1, 'name': 'Adorable Kitten'}, 'card_id': 1, 'collection_card_id': 14, 'quantity': 1, 'user_id': 2}

		for deck_card in deck.main_deck:
			card = Card.query.filter_by(card_id = deck_card.card_id).first()
			for dic in tmp_collection:
				card_id = dic['card_id']
				if card_id == card.card_id:
					if dic['quantity'] > deck_card.quantity:
						dic['quantity'] -= deck_card.quantity
					else:
						dic['quantity'] = 0

		for deck_card in deck.sideboard:
			card = Card.query.filter_by(card_id = deck_card.card_id).first()
			for dic in tmp_collection:
				card_id = dic['card_id']
				if card_id == card.card_id:
					if dic['quantity'] > deck_card.quantity:
						dic['quantity'] -= deck_card.quantity
					else:
						dic['quantity'] = 0

		return tmp_collection

	# @staticmethod
	# def user_collection_to_tmp_collection(collection):
	# 	new_collection = {}
	# 	for dictionary in collection:
	# 		card_id = dictionary['card_id']
	# 		quantity = dictionary['quantity']
	# 		name = dictionary['card']['name']
	# 		new_collection[card_id] = (name,quantity)
	# 	return new_collection


	@staticmethod
	def add_deck_to_tmp(deck, tmp_collection):
		"""
		: for every card in the deck, add each card and it's quantity
		: to this collection
		: No return value
		"""
		#{'card': {'card_id': 1, 'name': 'Adorable Kitten'}, 'card_id': 1, 'collection_card_id': 14, 'quantity': 1, 'user_id': 2}
		for deck_card in deck.main_deck:
			card = Card.query.filter_by(card_id = deck_card.card_id).first()
			added_flag = 0
			for dic in tmp_collection:
				card_id = dic['card_id']
				if card_id == card.card_id:
					dic['quantity'] += deck_card.quantity
					added_flag = 1
			if not added_flag:
				dic_to_add = {'card': {'card_id': card.card_id, 'name': card.name}, 'card_id': card.card_id, 'quantity':deck_card.quantity}
				tmp_collection.append(dic_to_add)


		for deck_card in deck.sideboard:
			card = Card.query.filter_by(card_id = deck_card.card_id).first()
			added_flag = 0
			for dic in tmp_collection:
				card_id = dic['card_id']
				if card_id == card.card_id:
					dic['quantity'] += deck_card.quantity
					added_flag = 1
			if not added_flag:
				dic_to_add = {'card': {'card_id': card.card_id, 'name': card.name}, 'card_id': card.card_id, 'quantity':deck_card.quantity}
				tmp_collection.append(dic_to_add)

		return tmp_collection

	@staticmethod
	def create_deck(**kwargs):
		"""
		: if either maindeck or sideboard exists, then add the corresponding 
		: DeckCard objects to match them.
		: Both will be input as lists of dictionaries 
		: For example 
		: main_deck = [
		: 	{"name", "Scalding Tarn", "quantity" : 4},
		:	....
		:	{"name", "Steam Vents", "quantity" : 2}
		: 	]
		: is a sample input
		: 
		: We have this in the constructor since we don't plan on editing decks once
		: they are made. Hence there is no add/remove card form deck method
		"""
		name = kwargs.get("name")
		event_placing = kwargs.get("event_placing")
		event = kwargs.get("event")
		main_deck = kwargs.get("main_deck")
		sideboard = kwargs.get("sideboard")
		player = kwargs.get("player")
		deck_id = kwargs.get("deck_id")
		archetype = kwargs.get("archetype")
		url = kwargs.get("url")

		# check if the deck is already in the database
		prev_deck = Deck.query.filter_by(deck_id = deck_id).first()
		if prev_deck:
			return prev_deck

		new_deck = Deck(
			url = url,
			name = name, event_placing = event_placing, 
			event_id = event.event_id, player = player, 
			deck_id = deck_id, archetype = archetype
		)

		db.session.add(new_deck)
		db.session.commit()
		if main_deck:
			for card in main_deck:
				if card["quantity"] == 0:
					continue
				search_card = Card.search_card_by_name(card['name'])
				if search_card:
					deck_id = new_deck.deck_id
					quantity = card['quantity']
					is_main_deck = True
					new_deck_card = DeckCard(card_id = search_card.card_id, deck_id = deck_id, quantity = quantity, is_main_deck = is_main_deck)
					db.session.add(new_deck_card)


		if sideboard:
			for card in sideboard:
				if card["quantity"] == 0:
					continue
				search_card = Card.search_card_by_name(card['name'])
				if search_card:
					deck_id = new_deck.deck_id
					quantity = card['quantity']
					is_main_deck = False
					new_deck_card = DeckCard(card_id = search_card.card_id, deck_id = deck_id, quantity = quantity, is_main_deck = is_main_deck)
					db.session.add(new_deck_card)
		db.session.commit()
		return new_deck

	@staticmethod
	def get_decks(page):
		DECKS_PER_PAGE = 10
		if page is not None:
			matching_decks = Deck.query.limit(page*DECKS_PER_PAGE).all()
		else:
			matching_decks = Deck.query.all()
		archetypes = set()
		length = Deck.query.count()
		output = []
		for deck in matching_decks:
			deck_dic = {'deck_id': deck.deck_id,
			'name': deck.name,
			'url': deck.url,
			'archetype': deck.archetype,
			'deck': deck.serialize(),
			}
			output.append(deck_dic)
			archetypes.add(deck.archetype)
		offset = 0
		if length%10 != 0:
			offset = 1

		return output, length//DECKS_PER_PAGE + offset, sorted(list(archetypes))

	def __repr__(self):
		return '<Deck %r %r %r>' % (self.name, self.event_placing, self.event_id)

	def serialize(self):
		"""
		: Returns the deck object in dictionary form, including the main_deck and sideboard
		:
		"""
		output = {'maindeck': [],
		'sideboard': [],
		'deck_id': self.deck_id,
		'url': self.url,
		'name': self.name
		}

		for card in self.main_deck:
			output['maindeck'].append(card.card.serialize())

		for card in self.sideboard:
			output['sideboard'].append(card.card.serialize())

		return output

		



